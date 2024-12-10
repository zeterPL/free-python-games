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
        "Game --> Tank : manages",
        "Game --> AITank : manages",
        "Game --> Bonus : manages",
        "Game --> Bullet : manages",
        "Game --> Tile : uses",
        "Game --> File : loads",
        "Game --> Draw : uses",
        "Game --> GameMode : has",
        "Tank <|-- AITank : inherits",
        "Bonus --> BonusType : has"
    ])
    umlLines.append("@enduml")
    return "\n".join(umlLines)


# Example of how to use the function with files
uploadedFiles = [
    "game.py",
    "tank.py",
    "tile.py",
    "file.py",
    "draw.py",
    "bullet.py",
    "bonus.py",
    "aiTank.py",
]

# Generate UML content
umlContent = generateUML(uploadedFiles)

# Save to a file
umlFilePath = "files/diagrams/diagram7.puml"
with open(umlFilePath, "w", encoding="utf-8") as umlFile:
    umlFile.write(umlContent)

print(f"UML file saved to {umlFilePath}")
