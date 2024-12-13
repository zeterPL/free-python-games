import os
import sys
import ast


def generateUML(files):
    umlLines = ["@startuml"]
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    # Determine if the class is an Enum
                    isEnum = any(base.id == "Enum" for base in node.bases if isinstance(base, ast.Name))
                    classType = "enum" if isEnum else "class"
                    # Start defining the class or enum
                    umlLines.append(f"{classType} {node.name} {{")
                    # Collect attributes and methods
                    attributes = []
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            if item.name == "__init__" and not isEnum:
                                # Collect attributes from __init__
                                for stmt in item.body:
                                    if isinstance(stmt, ast.Assign):
                                        for target in stmt.targets:
                                            if isinstance(target, ast.Attribute) and isinstance(target.value,
                                                                                                ast.Name) and target.value.id == "self":
                                                # Detect type from value
                                                attrType = "unknown"
                                                if isinstance(stmt.value, ast.List):
                                                    attrType = "list"
                                                elif isinstance(stmt.value, ast.Dict):
                                                    attrType = "dict"
                                                elif isinstance(stmt.value, ast.Str):
                                                    attrType = "str"
                                                elif isinstance(stmt.value, ast.Num):
                                                    attrType = "int"
                                                elif isinstance(stmt.value, ast.NameConstant):
                                                    attrType = "bool" if isinstance(stmt.value.value,
                                                                                    bool) else "NoneType"
                                                elif isinstance(stmt.value, ast.Call):
                                                    attrType = stmt.value.func.id if isinstance(stmt.value.func,
                                                                                                ast.Name) else "object"
                                                attributes.append(f"- {target.attr} : {attrType}")
                            elif not isEnum:
                                # Add method
                                args = ", ".join(arg.arg for arg in item.args.args if arg.arg != "self")
                                methods.append(f"  + {item.name}({args})")
                        elif isinstance(item, ast.Assign):
                            # Collect class-level attributes or enum members
                            for target in item.targets:
                                if isinstance(target, ast.Name):
                                    if isEnum and isinstance(item.value, ast.Constant):
                                        attributes.append(f"+ {target.id} = {item.value.value}")
                                    elif isEnum:
                                        attributes.append(f"+ {target.id} = unknown")
                                    else:
                                        attributes.append(f"- {target.id} : unknown")
                    # Add attributes or enum members to the class
                    for attr in attributes:
                        umlLines.append(attr)
                    # Add methods to the class
                    if not isEnum:
                        for method in methods:
                            umlLines.append(method)
                    # Close the class or enum definition
                    umlLines.append("}")
    # Add relationships
    umlLines.extend([
        "Game \"1\" *-- \"*\" Tank",
        "Game \"1\" *-- \"*\" Bullet",
        "Game \"1\" *-- \"*\" Bonus",
        "Game \"1\" *-- \"1\" GameMode",
        "Tank --> Game",
        "Tank <|-- AITank",
        "Tank \"1\" o-- \"*\" BonusType",
        "Bullet --> Tank",
        "Bonus --> Game",
        "Bonus \"1\" o-- \"*\" BonusType",
        "Tile <.. Game",
        "Tile <.. Draw",
        "File <.. Game",
        "Utils <.. Game",
        "Utils <.. Tank",
        "Draw <.. Game",
        "Draw <.. Tank",
        "Utils <.. Draw",
        "Vector <.. Game",
        "Vector <.. Tank",
        "Vector <.. Bonus",
        "Vector <.. Bullet",
    ])
    umlLines.append("@enduml")
    return "\n".join(umlLines)


if __name__ == "__main__":
    # Ustawienie ścieżki projektu jako katalogu głównego
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SRC_DIR = os.path.join(BASE_DIR, "src")
    # Dodanie katalogu src do sys.path, aby widzieć moduły z katalogu src
    sys.path.append(SRC_DIR)

    uploadedFiles = [
        os.path.join(SRC_DIR, "game.py"),
        os.path.join(SRC_DIR, "tank.py"),
        os.path.join(SRC_DIR, "tile.py"),
        os.path.join(SRC_DIR, "file.py"),
        os.path.join(SRC_DIR, "draw.py"),
        os.path.join(SRC_DIR, "bullet.py"),
        os.path.join(SRC_DIR, "bonus.py"),
        os.path.join(SRC_DIR, "aiTank.py"),
        os.path.join(SRC_DIR, "utils.py"),
    ]

    # Generate UML content
    umlContent = generateUML(uploadedFiles)

    # Save to a file
    umlFilePath = "diagram.puml"
    with open(umlFilePath, "w", encoding="utf-8") as umlFile:
        umlFile.write(umlContent)

    print(f"UML file saved to {umlFilePath}")
