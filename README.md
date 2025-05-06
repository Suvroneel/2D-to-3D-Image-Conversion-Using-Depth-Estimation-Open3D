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


3. Create and activate your environment, then install dependencies:

    > pip install -r requirements.txt

4. Run the script (e.g., from Spyder or command line):

    >python CODE/main.py





# 2. Libraries Used 

1. torch – For inference with the depth estimation model.

2. transformers – To load the GLPN model (vinvino02/glpn-nyu).

3. Pillow – For image loading and resizing.

4. matplotlib – For visualization.

5. numpy – For processing image and depth data.

6. open3d – For creating 3D point clouds and meshes.

7. pyplot (TkAgg backend) – Used with Spyder IDE for inline plotting.

8. rembg – For automatic background removal from images.

9. onnxruntime – For running inference with ONNX models (required by rembg).

# 3. Thought Process

###  1.  Input Image Preprocessing

1. Loaded the input image and removed the background using rembg to isolate the foreground object.

2. Resized the image and mask to fit the GLPN model’s input requirements while preserving aspect ratio.

###  2. Depth Estimation

1. Used the pretrained GLPN model to generate a depth map from the masked image.

2. Post-processed the depth map by cropping padding and applied the foreground mask to exclude background pixels.

###  3. 3D Reconstruction

1. Converted the masked image and depth map into an Open3D RGBD image.

2. Created a point cloud from the RGBD data and cleaned it using statistical outlier removal to eliminate noise.

###  4. Mesh Generation

1. Estimated surface normals and reconstructed a 3D mesh using Poisson surface reconstruction.

2. Rotated the mesh for better viewing alignment and exported it as a .obj file for external visualization.

###  5. Visualization

1. Generated an interactive 3D plot of the mesh using Matplotlib for quick validation.
2. Due to hardware limitations, I was unable to display the interactive plot directly on my machine. To ensure the results are still accessible and reviewable, I exported the 3D visualization as a PNG image file, which is included in the repository and showcased below.

# 4. Input and Output
-  Input image 



<img src="https://github.com/user-attachments/assets/22b4049e-b60a-4999-804b-2a2d6d34b375" alt="Image" width="300"></br>


 
 
 
 -  Output 3D image


https://github.com/user-attachments/assets/149820f3-5ef2-47de-927b-60077fd8c970




-   Visualization

![Image](https://github.com/user-attachments/assets/8b06b175-742d-4f30-a20c-bb9233c53f82)

*Note: The 3D mesh visualization was exported as a PNG file using Matplotlib, as my system could not render the interactive plot in real time. This approach ensures that the output remains accessible for review regardless of hardware limitations.*
