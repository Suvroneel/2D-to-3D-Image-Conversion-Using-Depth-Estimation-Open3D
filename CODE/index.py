#1. Libraries 
import matplotlib
matplotlib.use('TkAgg')

from matplotlib import pyplot as plt

from PIL import Image
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import torch
from transformers import GLPNImageProcessor, GLPNForDepthEstimation

#%% 2. Getting model
feature_extractor = GLPNImageProcessor.from_pretrained("vinvino02/glpn-nyu")
model = GLPNForDepthEstimation.from_pretrained("vinvino02/glpn-nyu")

#%% 3. Loadng Image
#image =Image.open("../DATA/car.jpg")
image =Image.open("../DATA/toy.jpg")
 
new_height = 480 if image.height > 480 else image.height
new_height -=(new_height % 32)
new_width = int(new_height * image.width / image.height)
diff = new_width % 32

new_width = new_width - diff if diff < 16 else new_width +32 - diff
new_size=(new_width,new_height)
image = image.resize(new_size)

#%% 4. preparing image for model 

inputs = feature_extractor(images = image , return_tensors = "pt")

#%%5. Getting the prediction from the model 
with torch.no_grad():
    outputs = model(**inputs)
    predicted_depth = outputs.predicted_depth


#%%6. Post-processing

pad = 16

output = predicted_depth.squeeze().cpu().numpy() * 1000.0
output = output[pad:-pad, pad:-pad]
image = image.crop((pad, pad, image.width - pad, image.height - pad))



# visualize the prediction

fig, ax = plt.subplots(1, 2)
ax[0].imshow(image)
ax[0].tick_params(left=False, bottom = False, labelleft=False, labelbottom=False)

ax[1].imshow(output, cmap='plasma')

ax[1].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

plt.tight_layout()

plt.pause(5)

#%%7. importing Libs

import numpy as np
import open3d as o3d

#%% 8. preparing the depth image for open3d

width, height = image.size
depth_image = (output *255 / np.max(output)).astype('uint8')#8 bits
image = np.array(image)

#create rgbd image
depth_o3d= o3d.geometry.Image(depth_image)
image_o3d =o3d.geometry.Image(image)
rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(image_o3d,depth_o3d ,
convert_rgb_to_intensity=False)

#%%9 Creating Camera (Projection Matrix)

camera_intrinsic = o3d.camera.PinholeCameraIntrinsic()
camera_intrinsic.set_intrinsics(width ,height ,500 ,500 ,width/2 ,height/2)


#%%10 Creating O3D point cloud (the 3d image)

pcd_raw = o3d.geometry.PointCloud().create_from_rgbd_image(rgbd_image , camera_intrinsic)

o3d.visualization.draw_geometries([pcd_raw])


#%%11 Post processing 3D imgae 

cl , ind = pcd_raw.remove_statistical_outlier(nb_neighbors=20, std_ratio= 6.0)
pcd =pcd_raw.select_by_index(ind)

#estimate normals
pcd.estimate_normals()
pcd.orient_normals_to_align_with_direction()

o3d.visualization.draw_geometries([pcd_raw])



#%%12 Surface reconstruction 

mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd ,
depth= 10 , n_threads=1)[0]

#rotate the mesh
rotation= mesh.get_rotation_matrix_from_xyz((np.pi,0,0))
mesh.rotate(rotation , center =(0 ,0 ,0))


#visualize mesh 

o3d.visualization.draw_geometries([mesh],mesh_show_back_face= True)


#%%13 Exporting the mesh and 3d Graph

#o3d.io.write_triangle_mesh('../RESULT/Car3D.obj', mesh)
o3d.io.write_triangle_mesh('../RESULT/Toy3D.obj', mesh)

#For viewing the mesh with colors 
#o3d.io.write_triangle_mesh('../RESULT/Toy3D.ply', mesh)


# Extract mesh data
vertices = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)

# Basic 3D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

mesh_collection = Poly3DCollection(vertices[triangles], alpha=0.7)
mesh_collection.set_edgecolor('k')
ax.add_collection3d(mesh_collection)

# Set axis limits
ax.set_xlim(vertices[:, 0].min(), vertices[:, 0].max())
ax.set_ylim(vertices[:, 1].min(), vertices[:, 1].max())
ax.set_zlim(vertices[:, 2].min(), vertices[:, 2].max())

ax.set_title('3D Mesh Visualization')
plt.tight_layout()
plt.show()

#plt.savefig("../RESULT/3D_mesh_plot.png")
 



