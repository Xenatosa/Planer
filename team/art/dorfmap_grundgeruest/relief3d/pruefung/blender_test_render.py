# Headless-Test: blender -b -P blender_test_render.py -- dorfmap_O17.glb ausgabe.png [WORKBENCH|CYCLES]
import bpy,sys,math,mathutils
a=sys.argv[sys.argv.index('--')+1:];glb,out=a[0],a[1];eng=a[2] if len(a)>2 else 'CYCLES'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
obs=[o for o in bpy.context.scene.objects if o.type=='MESH']
print('OBJEKTE',len(obs),[(o.name,len(o.data.polygons),list(o.data.color_attributes.keys())) for o in obs])
lo=[min((o.matrix_world@mathutils.Vector(c))[i] for o in obs for c in o.bound_box) for i in range(3)]
hi=[max((o.matrix_world@mathutils.Vector(c))[i] for o in obs for c in o.bound_box) for i in range(3)]
print('BBOX_m',lo,hi)
for o in obs:   # Material: Vertexfarbe direkt
    m=bpy.data.materials.new(o.name);m.use_nodes=True;nt=m.node_tree;bs=nt.nodes['Principled BSDF']
    ca=nt.nodes.new('ShaderNodeVertexColor');nt.links.new(ca.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=0.9
    o.data.materials.clear();o.data.materials.append(m)
sc=bpy.context.scene;cx,cy=(lo[0]+hi[0])/2,(lo[1]+hi[1])/2
cam=bpy.data.objects.new('kam',bpy.data.cameras.new('kam'));sc.collection.objects.link(cam);sc.camera=cam
cam.location=(cx,cy-330,260);cam.rotation_euler=(math.radians(52),0,0);cam.data.lens=28;cam.data.clip_end=3000
sun=bpy.data.objects.new('sonne',bpy.data.lights.new('sonne','SUN'));sun.data.energy=3.5;sun.rotation_euler=(math.radians(40),0,math.radians(30));sc.collection.objects.link(sun)
w=bpy.data.worlds.new('w');sc.world=w;w.color=(0.6,0.7,0.85)
sc.render.resolution_x,sc.render.resolution_y=1280,800;sc.render.filepath=out
if eng=='WORKBENCH':sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.color_type='VERTEX';sc.display.shading.light='STUDIO'
else:sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=16;sc.cycles.use_denoising=False
bpy.ops.render.render(write_still=True);print('GERENDERT',out)
