# UliPipe Documentation

> WARNING: This pipeline tool only works with the ESMA default pipeline structure

## Installation Procedure

- To install this pipeline manager, simply drag & drop it in your maya viewport, and you should be all set!
#
#### ```Have Fun !```
#
## Usage

### 1. Path (PATH)

### The first thing to do when starting to work on a new project is setting the path 

- To set the path, click the PATH button and select the root folder of your project
- When changing computers, or moving the root pipeline folder, this step must be done again


### 2. Create Asset (crAsset)

- This button allows you to create an asset
- To do so, just specify an asset type(character, FX, item, prop, or set) and a name for the asset
- This will throw an error if an asset with the same name already exists, or the name is empty, or other things, just dont mess up


### 3. Open Asset (opAsset)

- This button allows you to open an asset
- Just specify the type, name and department and the tool will open the latest edit for you
- If there are no edit files for this department, the tool will create the first one and open it for you


### 4. Create Shot (crShot)

- This button allows you to create a shot
- To do so, just specify sequence and shot numbers for the shot
- This will throw an error if a shot with the same name already exists, or other things, just dont mess up


### 5. Open Shot (opShot)

- This button allows you to open a shot
- Just specify the shot name and department and the tool will open the latest edit for you
- If there are no edit files for this department, the tool will create the first one and open it for you


### 6. Edit (EDIT)

- The edit button allows you to automatically save an incremented version of your current file
- This only works with the default ESMA naming such as: ```myAsset_department_E_myVersion.ma```
- If the action cannot be completed, the button will throw an error
- The button will throw an error if: the file is not in the project, the file is not named properly, and if the file is not the latest increment


### 7. Publish (PUB)

- The publish button publishes your current file to the pipeline
- If this asset already has a publish in the given department, the tool will move the old publish to a backup folder
- If the action cannot be completed, the button will throw an error
- The button will throw an error if: the file is not in the project, the file is not named properly


### 8.Reference Asset (REF)

- This button allows you to reference an asset in your current scene
- Just specify the type, name and department of the asset and the tool will reference the publish for you
- If there are no publish files for this department, the tool will throw an error


### 9. ? (?)

- Just click it...
