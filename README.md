 # "Ad Fontes" Research Project
 ## «Image backward contour tracing algorithm» for Algorithm and Linear Algebra courses.
 
+When you run ad_pontes.py you should choose image in folder with which you want to work.
+Then choose pixel which belongs to the object conotur of which you want to get. It's better to choose this pixel as close to the top right side as possible because then there is bigger chance program will not run into some unexpected problems and will work correctly. To confirm chosen pixel close the window and program will continue it's work.
+After this you will see resultat of segmantation of this image using Watershed algorithm. I used library cv2 to do this algorithm. All it does is that it draws contour around all objects it can detect as different objects. This algorithm helps overall program work better but it still isn't working perfectly. So even without it algorithm will work just fine. 
+At the end program will show image of contour pixels, time it took to execute this program, number of contour pixels and return them.
+With commands in cmd 

+>> ./python ad_fontes.py  'arg'
+you can run this program.
+Integer from 0 to 255 as argument will change range in which next pixel will be conted as contour pixel. Usually it shouldn't be used.
+Argument 'test' will run test which will return bct algorithm for 4 testing pictures.
+Argument 'save' will save contour of image as ad_fontes_contour.jpg.
+Argument 'steps' will be opening in gallery contour of image every 200 pixels.
 Made by [Shtohrinets Bohdan](https://github.com/Bodi44) and [Roman Stepaniuk](https://github.com/st-rom)
 # Video demonstration: https://drive.google.com/file/d/1USlwHTUDYsZyT0_vic6nXtbBBSYSfTBC/view?usp=sharing
