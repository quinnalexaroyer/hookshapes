# hookshapes
Python script for Blender 3D which creates vertex groups for hook modifiers that act like shape keys.

Once your mesh has been finished, run the script (hookshapes.py) and it will create a menu called "Hook Shapes" in the 3D view sidebar. Enter the name of the object in the "object" field and push "Run". This will create a text object called "storedata.txt" which will store the coordinates of your mesh. It will create another text document called "maxco.txt" that is initially blank and will be used later.

After you have pushed "Run", you can edit the vertices of your mesh as though you were creating a shape key. After you have finished moving the vertices and you have entered a name in the "group_name" field, push "Make Group". This will create six vertex groups for the mesh object. Their names will be what you entered under "group_name" plus the suffixes -X +X -Y +Y -Z +Z. Pushing "Make Group" will also move the vertices of your mesh back to the way they were (using the coordinates stored in the storedata.txt file). If you wish to discard the changes to your mesh while editing vertices you can push "Reset" in the sidebar and it will move the vertices back to the coordinates in storedata.txt without creating vertex groups.

Now you can create six hook modifiers on your mesh for each of the vertex groups the script created. I suggest creating armature bones to use as targets for the hook modifiers.
