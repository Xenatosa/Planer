# t48u R5: Fels-Grundformen mit headless Blender 4.2 (Displace Voronoi+Clouds, Decimate). Aufruf:
#   /tmp/blender-4.2.3-linux-x64/blender -b --python blender/fels_meshes.py   -> blender/fels_meshes.json
import bpy,json,os,random
out=[];D=os.path.dirname(os.path.abspath(__file__))
for v in range(8):
    bpy.ops.wm.read_factory_settings(use_empty=True);random.seed(v)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5,radius=0.6);o=bpy.context.active_object
    o.scale=(1+random.random()*0.5,0.7+random.random()*0.4,1+random.random()*0.3);bpy.ops.object.transform_apply(scale=True)
    for typ,st,sz in (('VORONOI',0.28,0.55+0.3*random.random()),('CLOUDS',0.10,0.25)):
        t=bpy.data.textures.new('t'+typ,typ)
        if typ=='VORONOI':t.distance_metric='DISTANCE';t.noise_intensity=1.0
        t.noise_scale=sz;m=o.modifiers.new('d'+typ,'DISPLACE');m.texture=t;m.strength=st;m.texture_coords='LOCAL'
    d=o.modifiers.new('dec','DECIMATE');d.ratio=0.08
    dg=bpy.context.evaluated_depsgraph_get();me=o.evaluated_get(dg).to_mesh();me.calc_loop_triangles()
    P=[round(c,4) for vv in me.vertices for c in (vv.co.x,vv.co.z,vv.co.y)];I=[i for t in me.loop_triangles for i in t.vertices]
    out.append({'p':P,'i':I});print('FELS',v,len(I)//3)
json.dump(out,open(D+'/fels_meshes.json','w'))
