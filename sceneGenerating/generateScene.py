import os
import platform
delim = '/' if 'Linux' in platform.system() else f'\\'
path = os.getcwd()
pathToModelDir = f"{os.path.dirname(path)}{delim}models{delim}"

model_cube = 'cube.obj'
pathToCube = f'{pathToModelDir}{model_cube}'
pathToCube = pathToCube.replace('\\', '/')

model_spring = 'spring.3DXML'
pathToSpring = f'{pathToModelDir}{model_spring}'
pathToSpring = pathToSpring.replace('\\', '/')


def generate_complete_file(n_cubes, n_springs, original_filename="patternForGenerating.vrcp", new_filename="outPutFile.vrcp"):
    # Read the original content
    with open(original_filename, "r") as file:
        original_content = file.read()

    # Locate the position to insert new nodes
    insert_pos = original_content.rfind("node\n\t{") + len("node\n\t{")

    # Generate new nodes string
    new_nodes = '''
    plugin = "StandardOsgLoader"
        property = "vrc::TransformProperty"
        property = "vrc::ModelLoaderProperty"
        property = "vrc::ShowHideProperty"

        model_loader
        {
            EnableBlending = "false"
            EnableLODs = "false"
            ForceNoBackfaceCulling = "false"
            ForceNormalizeNormals = "true"
            ModelName = "ObjectLibraryCachedModels"
            Rotate = "0 0 0"
            Scale = "1 1 1"
            Translate = "0 0 0"
        }}
'''
    # Define the ticker for cubes and springs separately
    ticker_cubes = 0
    ticker_springs = 0

    # Generate nodes for cubes
    for i in range(n_cubes):
        new_node = f'''
        node
        {{
            cached_model_guid = "2934EE4AEC487E4AAB9364D465F607B1"
            file = "{pathToCube}"
            property = "vrc::TransformProperty"
            property = "vrc::ModelLoaderProperty"
            property = "vrc::SimulatedProperty"

            model_loader
            {{
                EnableBlending = "false"
                EnableLODs = "false"
                ForceNoBackfaceCulling = "false"
                ForceNormalizeNormals = "true"
                ModelName = "cube{i}"
                Rotate = "0 0 0"
                Scale = "1 1 1"
                Translate = "0 0 0"
            }}

            simulated
            {{
                AttachWindowPosition = "false"
                CaptionText = ""
                FeedbackValueCount = "0"
                FeedbackValueStrings = ""
                GroupName = ""
                Overridable = "true"
                RemovePropertyOnClose = "false"
                ShowCaption = "false"
                ShowWindow = "true"
                ValueCount = "6"
                ValueStrings = "move:{i*6+1}:1:1,0,0;move:{i*6+2}:1:0,1,0;move:{i*6+3}:1:0,0,1;rotate:{i*6+4}:1:1,0,0;rotate:{i*6+5}:1:0,1,0;rotate:{i*6+6}:1:0,0,1"
                WindowPosition = "0 0 0"
                WindowRotate = "0 -0 0"
                WindowWidth = "0"
            }}

            transform
            {{
                ForceNormalizeNormals = "true"
                InitMatrix = "1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"
                Rotate = "0 -0 0"
                Scale = "1 1 1"
                Translate = "0 0 0"
            }}
        }}\n'''
        new_nodes += new_node
        ticker_cubes += 1

    # Update the ticker for springs based on the number of cubes added
    ticker_springs = ticker_cubes * 6

    # Generate nodes for springs
    for i in range(n_springs):
        new_node = f'''
        node
        {{
            cached_model_guid = "2934EE4AEC487E4AAB9364D465F607B1"
            file = "{pathToSpring}"
            property = "vrc::TransformProperty"
            property = "vrc::ModelLoaderProperty"
            property = "vrc::SimulatedProperty"

            model_loader
            {{
                EnableBlending = "false"
                EnableLODs = "false"
                ForceNoBackfaceCulling = "false"
                ForceNormalizeNormals = "true"
                ModelName = "spring{i}"
                Rotate = "0 0 0"
                Scale = "1 1 1"
                Translate = "0 0 0"
            }}

            simulated
            {{
                AttachWindowPosition = "false"
                CaptionText = ""
                FeedbackValueCount = "0"
                FeedbackValueStrings = ""
                GroupName = ""
                Overridable = "true"
                RemovePropertyOnClose = "false"
                ShowCaption = "false"
                ShowWindow = "true"
                ValueCount = "7"
                ValueStrings = "move:{ticker_springs+1}:1:1,0,0;move:{ticker_springs+2}:1:0,1,0;move:{ticker_springs+3}:1:0,0,1;rotate:{ticker_springs+4}:1.001:1,0,0;rotate:{ticker_springs+5}:1.001:0,1,0;rotate:{ticker_springs+6}:1.001:0,0,1;scale:{ticker_springs+7}:1:0,0,1"
                WindowPosition = "0 0 0"
                WindowRotate = "0 -0 0"
                WindowWidth = "0"
            }}

            transform
            {{
                ForceNormalizeNormals = "true"
                InitMatrix = "1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"
                Rotate = "0 -0 0"
                Scale = "1 1 1"
                Translate = "0 0 0"
            }}
        }}\n'''
        new_nodes += new_node
        ticker_springs += 7

    # Insert the new nodes into the original content
    complete_content = original_content[:insert_pos] + new_nodes + original_content[insert_pos:]

    # Write the modified content into a new file
    with open(new_filename, "w") as new_file:
        new_file.write(complete_content)

generate_complete_file(4,6)
