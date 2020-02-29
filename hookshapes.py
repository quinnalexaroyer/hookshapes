import bpy

def loadCoData(filename):
	txt = bpy.data.texts["storedata.txt"]
	l = txt.as_string().split("\n")
	pts = [0]*len(l)
	for i in l:
		i0 = i.split(": ")
		if len(i) > 1: pts[int(i0[0])] = [float(j) for j in i0[1][1:-1].split(",")]
	return pts

def storeData():
	txt = bpy.data.texts["storedata.txt"]
	txt.from_string("")
	m = bpy.data.objects[getattr(bpy.context.scene,"object")].data
	for i in range(len(m.vertices)):
		txt.write(str(i)+": "+str(m.vertices[i].co[:])+"\n")

def makeGroup():
	txt = bpy.data.texts["storedata.txt"]
	o = bpy.data.objects[getattr(bpy.context.scene,"object")]
	m = o.data
	l = txt.as_string().split("\n")
	gv = []
	orig_vertices = []
	for i in l:
		i0 = i.split(": ")
		if len(i0) > 1:
			pt = [float(j) for j in i0[1][1:-1].split(",")]
			d = [0,0,0]
			for j in (0,1,2):
				d[j] = m.vertices[int(i0[0])].co[j] - pt[j]
			if d[0]**2+d[1]**2+d[2]**2 > 0.00001**2:
				gv.append((int(i0[0]),d))
			orig_vertices.append((int(i0[0]),pt))
	maxco = [0,0,0]
	minco = [0,0,0]
	if len(gv) >= 1:
		maxco[0] = max([i[1][0] for i in gv])
		maxco[1] = max([i[1][1] for i in gv])
		maxco[2] = max([i[1][2] for i in gv])
		minco[0] = min([i[1][0] for i in gv])
		minco[1] = min([i[1][1] for i in gv])
		minco[2] = min([i[1][2] for i in gv])
	groupname = getattr(bpy.context.scene,"group_name")
	basename = groupname
	extname = ""
	if groupname[-2:] in (".L",".R"):
		basename = groupname[:-2]
		extname = groupname[-2:]
	axisstr = ("X","Y","Z")
	maxcotext = bpy.data.texts["maxco.txt"]
	maxcotext.write(basename+extname+"\t"+str(maxco)+"\t"+str(minco)+"\n")
	for j in (0,1,2):
		if maxco[j] > 0.00001:
			newgroup = o.vertex_groups.new(name=basename+"+"+axisstr[j]+extname)
			for i in gv:
				if i[1][j] > 0.00001:
					newgroup.add([i[0]],i[1][j]/maxco[j],'REPLACE')
		if minco[j] < -0.00001:
			newgroup = o.vertex_groups.new(name=basename+"-"+axisstr[j]+extname)
			for i in gv:
				if i[1][j] < -0.00001:
					newgroup.add([i[0]],i[1][j]/minco[j],'REPLACE')
	resetMesh(m)

def loadGroup():
	o = bpy.data.objects[getattr(bpy.context.scene,"object")]
	m = o.data
	groupname = getattr(bpy.context.scene,"group_name")
	basename = groupname
	extname = ""
	if basename[-2:] in (".L",".R"):
		basename = groupname[:-2]
		extname = groupname[-2:]
	groupIndices = [o.vertex_groups[basename+i+extname].index if basename+i+extname in o.vertex_groups else None for i in ("+X","-X","+Y","-Y","+Z","-Z")]
	txt = bpy.data.texts["maxco.txt"]
	mm = []
	for l in [i.body for i in txt.lines]:
		if l.split("\t")[0] == groupname:
			mm = l.strip().split("\t")
	mv = ([float(i) for i in mm[1][1:-1].split(",")], [float(i) for i in mm[2][1:-1].split(",")])
	for v in m.vertices:
		for g in v.groups:
			axisIndex = -1
			for i in range(6):
				if groupIndices[i] is not None and g.group == groupIndices[i]:
					axisIndex = i
					print(g.group, o.vertex_groups[g.group], axisIndex)
			if axisIndex != -1:
				v.co[axisIndex//2] += g.weight*mv[axisIndex%2][axisIndex//2]
	print(groupIndices)

def resetMesh(m):
	txt = bpy.data.texts["storedata.txt"]
	pts = loadCoData("storedata.txt")
	for i in range(len(pts)):
		if isinstance(pts[i],list) and len(pts[i]) >= 3:
			for j in (0,1,2):
				m.vertices[i].co[j] = pts[i][j]

class DataPanel(bpy.types.Panel):
	bl_label = "Hook Shapes"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"

	def __init__(self):
		self.scn = bpy.context.scene

	def draw(self,context):
		layout = self.layout
		layout.prop(self.scn,"object")
		layout.operator("data.run", text="Run")
		layout.prop(self.scn,"group_name")
		layout.operator("data.makegroup", text="Make Group")
		layout.operator("data.load", text="Load")
		layout.operator("data.reset", text="Reset")

class DATA_OT_run(bpy.types.Operator):
	bl_idname = "data.run"
	bl_label = "Run"
	def execute(self,context):
		storeData()
		return{'FINISHED'}

class DATA_OT_makegroup(bpy.types.Operator):
	bl_idname = "data.makegroup"
	bl_label = "Make Group"
	def execute(self,context):
		makeGroup()
		return{'FINISHED'}

class DATA_OT_load(bpy.types.Operator):
	bl_idname = "data.load"
	bl_label = "Load"
	def execute(self,context):
		loadGroup()
		return{'FINISHED'}

class DATA_OT_reset(bpy.types.Operator):
	bl_idname = "data.reset"
	bl_label = "Reset"
	def execute(self,context):
		m = bpy.data.objects[getattr(bpy.context.scene,"object")].data
		resetMesh(m)
		return{'FINISHED'}

setattr(bpy.types.Scene, "object", bpy.props.StringProperty(name="object", default=""))
setattr(bpy.types.Scene, "group_name", bpy.props.StringProperty(name="group_name", default=""))
bpy.utils.register_class(DATA_OT_run)
bpy.utils.register_class(DATA_OT_makegroup)
bpy.utils.register_class(DATA_OT_load)
bpy.utils.register_class(DATA_OT_reset)
bpy.utils.register_class(DataPanel)
if "storedata.txt" not in bpy.data.texts:
	bpy.data.texts.new("storedata.txt")
if "maxco.txt" not in bpy.data.texts:
	bpy.data.texts.new("maxco.txt")
