# t54u: Versuch zusammenhaengendes Wandband-Mesh mit Blender (Displace Voronoi/Stucci-Schichten + Voxel-Remesh) [A]
# Aufruf: FW_NPZ=/tmp/fw.npz blender -b --python blender/wandband_t54u.py -- OUT_DIR
import bpy,os,sys,numpy as np,bmesh
OUT=sys.argv[sys.argv.index('--')+1];Z=np.load(os.environ['FW_NPZ'])
FH,vin=Z['FH'],Z['vin'];FS=4;W=120   # Ausschnitt 30 m x 30 m
best=None
for y in range(0,FH.shape[0]-W,40):
    for x in range(0,FH.shape[1]-W,40):
        v=vin[y:y+W,x:x+W];c=v.sum()
        if c>0.55*W*W and FH[y:y+W,x:x+W].ptp()>11 and (best is None or c>best[0]):best=(c,y,x)
_,y0,x0=best;P=FH[y0:y0+W,x0:x0+W].astype(float);print('AUSSCHNITT',y0,x0,P.min(),P.max())
def grid(name,H):
    me=bpy.data.meshes.new(name);n=H.shape[0]
    V=[(i/FS,j/FS,H[j,i]) for j in range(n) for i in range(n)];F=[(j*n+i,j*n+i+1,(j+1)*n+i+1,(j+1)*n+i) for j in range(n-1) for i in range(n-1)]
    me.from_pydata(V,[],F);o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);return o
def kamera_licht():
    c=bpy.data.objects.new('cam',bpy.data.cameras.new('cam'));bpy.context.collection.objects.link(c);bpy.context.scene.camera=c
    import mathutils;ctr=mathutils.Vector((W/FS/2,W/FS/2,(P.min()+P.max())/2))
    # Blick quer zur mittleren Fallrichtung
    gy,gx=np.gradient(P);d=mathutils.Vector((-gx.mean(),-gy.mean(),0)).normalized()
    c.location=ctr+d*46+mathutils.Vector((0,0,9));c.rotation_euler=(ctr-c.location).to_track_quat('-Z','Y').to_euler()
    s=bpy.data.objects.new('sun',bpy.data.lights.new('sun','SUN'));s.data.energy=4.5;sd=(d+mathutils.Vector((-d.y,d.x,0))*2.2+mathutils.Vector((0,0,1.1))).normalized();s.rotation_euler=sd.to_track_quat('Z','Y').to_euler();bpy.context.collection.objects.link(s)   # Streiflicht von der Seite
    w=bpy.data.worlds.new('w');w.color=(0.18,0.2,0.25);bpy.context.scene.world=w
def mat(o):
    m=bpy.data.materials.new('fels');m.use_nodes=True;b=m.node_tree.nodes['Principled BSDF'];b.inputs['Base Color'].default_value=(0.42,0.40,0.38,1);b.inputs['Roughness'].default_value=0.9
    o.data.materials.append(m)
def render(fn):
    sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=12;sc.render.resolution_x=800;sc.render.resolution_y=500
    sc.render.filepath=fn;bpy.ops.render.render(write_still=True)
for variante in ('feinrelief','blender'):
    bpy.ops.wm.read_factory_settings(use_empty=True);o=grid('w',P);bpy.context.view_layer.objects.active=o;o.select_set(True)
    if variante=='blender':
        sol=o.modifiers.new('sol','SOLIDIFY');sol.thickness=4;sol.offset=-1
        bpy.ops.object.modifier_apply(modifier='sol')
        for typ,st,sz in (('STUCCI',0.9,2.5),('VORONOI',1.4,3.5),('CLOUDS',0.35,0.8)):
            t=bpy.data.textures.new(typ,typ);t.noise_scale=sz
            if typ=='VORONOI':t.distance_metric='DISTANCE_SQUARED'
            m=o.modifiers.new(typ,'DISPLACE');m.texture=t;m.strength=st;m.texture_coords='LOCAL';m.mid_level=0.5
        r=o.modifiers.new('rm','REMESH');r.mode='VOXEL';r.voxel_size=0.25
        d=o.modifiers.new('dec','DECIMATE');d.ratio=0.35
        for mm in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=mm.name)
    bpy.ops.object.shade_smooth();mat(o);print('DREIECKE',variante,sum(len(p.vertices)-2 for p in o.data.polygons))
    kamera_licht();render(os.path.join(OUT,'bl_'+variante+'.png'))
