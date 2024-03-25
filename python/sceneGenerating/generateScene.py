import os
import platform
delim = '/' if 'Linux' in platform.system() else f'\\'
path = os.getcwd()
pathToModelDir = f"{os.path.dirname(os.path.dirname(path))}{delim}models{delim}"

model = 'cube.obj'
pathToMainModel = f'{pathToModelDir}{model}'
pathToMainModel = pathToMainModel.replace('\\', '/')



# Let's define a function to add new models to the existing scene_manager section
def generate_complete_file(n, original_filename="patternForGenerating.vrcp", new_filename="outPutFile.vrcp"):
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
    for i in range(n):
        new_node = f'''
\t\t\tnode
\t\t\t{{
\t\t\t\tcached_model_guid = "2934EE4AEC487E4AAB9364D465F607B1"
\t\t\t\tfile = "{pathToMainModel}"
\t\t\t\tproperty = "vrc::TransformProperty"
\t\t\t\tproperty = "vrc::ModelLoaderProperty"
\t\t\t\tproperty = "vrc::SimulatedProperty"

\t\t\t\tmodel_loader
\t\t\t\t{{
\t\t\t\t\tEnableBlending = "false"
\t\t\t\t\tEnableLODs = "false"
\t\t\t\t\tForceNoBackfaceCulling = "false"
\t\t\t\t\tForceNormalizeNormals = "true"
\t\t\t\t\tModelName = "cube{i}"
\t\t\t\t\tRotate = "0 0 0"
\t\t\t\t\tScale = "1 1 1"
\t\t\t\t\tTranslate = "0 0 0"
\t\t\t\t}}

\t\t\t\tsimulated
\t\t\t\t{{
\t\t\t\t\tAttachWindowPosition = "false"
\t\t\t\t\tCaptionText = ""
\t\t\t\t\tFeedbackValueCount = "0"
\t\t\t\t\tFeedbackValueStrings = ""
\t\t\t\t\tGroupName = ""
\t\t\t\t\tOverridable = "true"
\t\t\t\t\tRemovePropertyOnClose = "false"
\t\t\t\t\tShowCaption = "false"
\t\t\t\t\tShowWindow = "true"
\t\t\t\t\tValueCount = "6"
\t\t\t\t\tValueStrings = "move:{i*6+1}:1:1,0,0;move:{i*6+2}:1:0,1,0;move:{i*6+3}:1:0,0,1;rotate:{i*6+4}:1:1,0,0;rotate:{i*6+5}:1:0,1,0;rotate:{i*6+6}:1:0,0,1"
\t\t\t\t\tWindowPosition = "0 0 0"
\t\t\t\t\tWindowRotate = "0 -0 0"
\t\t\t\t\tWindowWidth = "0"
\t\t\t\t}}

\t\t\t\ttransform
\t\t\t\t{{
\t\t\t\t\tForceNormalizeNormals = "true"
\t\t\t\t\tInitMatrix = "1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"
\t\t\t\t\tRotate = "0 -0 0"
\t\t\t\t\tScale = "1 1 1"
\t\t\t\t\tTranslate = "0 0 0"
\t\t\t\t}}
\t\t\t}}\n'''
        new_nodes += new_node

    # Insert the new nodes into the original content
    complete_content = original_content[:insert_pos] + new_nodes + original_content[insert_pos:]

    # Write the modified content into a new file
    with open(new_filename, "w") as new_file:
        new_file.write(complete_content)

# Assuming 'original_file.rcp' exists and contains the provided content,
# this will add 5 new models to it and save as 'complete_file.rcp'
generate_complete_file(7)
