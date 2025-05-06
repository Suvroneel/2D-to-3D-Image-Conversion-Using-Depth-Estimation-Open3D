# 3D Image reconstruction from 2D image
A Python prototype that converts 2D photos or text prompts into 3D models (.ply) using depth estimation and surface reconstruction. 

# 1.Steps to run
1. Clone the repository and navigate to the project root.

2. Ensure your folders are structured like:

── CODE/

    └── main.py


── DATA/


    └── toy.jpg  # or any input image


── RESULT/

    └── Toy3D.ply  # Output mesh


3. Activate your environment, then install dependencies:

    > pip install -r requirements.txt

4. Run the script (e.g., from Spyder or command line):

    >python CODE/main.py





# 2. Libraries Used 

torch – for inference with the depth estimation model

transformers – to load GLPN model (vinvino02/glpn-nyu)

Pillow – for image loading and resizing

matplotlib – for visualization

numpy – for processing image/depth data

open3d – for creating 3D point cloud and mesh

pyplot (TkAgg backend) – used with Spyder IDE for inline plotting

rembg – For automatic background removal from images

# 3. Thought Process

1. I started by resizing and formatting the 2D input image.

2. Used a pretrained GLPN model to estimate depth, then converted the result into an Open3D-compatible RGBD image.
  
3. Created a point cloud and cleaned it using statistical outlier removal.

4. Estimated normals and generated a mesh using Poisson surface reconstruction.

5. Rotated the mesh for better view alignment and exported it as a .ply file  for external viewing

6. A 3D graph of the generated mesh is visualized using Matplotlib. This provides an interactive way to view the 3D mesh, adding an extra layer of detail to the project.
