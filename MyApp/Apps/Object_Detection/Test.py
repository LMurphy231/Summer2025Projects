from PIL import Image
import os

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.save_base_folder = r"MyApp\Apps\Object_Detection\Images"
        self.get_pixel_data()
        self.width, self.height = self.image.size

        self.GR_Ratio = []
        self.BR_Ratio = []
        self.R_Ratio = []

        self.RG_Ratio = []
        self.BG_Ratio = []
        self.G_Ratio = []

        self.RB_Ratio = []
        self.GB_Ratio = []
        self.B_Ratio = []

        self.grayscale_pixel_data=[]
    
        self.RED = 0
        self.GREEN = 1
        self.BLUE = 2

        #initial functions
        self.convert_to_grayscale()
        self.grayscale_convert_to_bw(0.2)
        self.refine_area(self.BW_pixel_data,1,0.1)
        self.find_edge(self.refined_pixels)
        self.blur_image(self.pixel_data, 4)
    
        self.get_rgb_ratio()

        self.pixels_to_image(self.ratios[self.RED], "RED")
        self.pixels_to_image(self.ratios[self.GREEN], "GREEN")
        self.pixels_to_image(self.ratios[self.BLUE], "BLUE")

        self.pixels_to_image(self.RG_Ratio, "REDGREEN")
        self.pixels_to_image(self.GB_Ratio, "GREENBLUE")
        self.pixels_to_image(self.BR_Ratio, "BLUERED")


        #self.refine_area(self.BWpixels,1,0.5)

    def get_pixel_data(self):
        try:
            self.image = Image.open(self.image_path)
            self.image = self.image.convert("RGB")
            self.pixel_data = list(self.image.getdata())
        except FileNotFoundError:
            print(f"Error: Image File not found at {self.image_path}")
            return None
        except Exception as e:
            print(f"An error has occured: {e}")
            return None
    
    def get_rgb_ratio(self):
        RED = 0
        GREEN = 1
        BLUE = 2

        for index, pixel in enumerate(self.pixel_data):
            if pixel[RED] != 0:                             #will avoid NULLS
                self.GR_Ratio.append(pixel[GREEN]/pixel[RED])
                self.BR_Ratio.append(pixel[BLUE]/pixel[RED])
                self.R_Ratio.append(self.GR_Ratio[index] + self.BR_Ratio[index])
            else:                                               #Set NULLS as None
                self.GR_Ratio.append(0)
                self.BR_Ratio.append(0)
                self.R_Ratio.append(0)

            if pixel[GREEN] != 0:                             #will avoid NULLS
                self.RG_Ratio.append(pixel[RED]/pixel[GREEN])
                self.BG_Ratio.append(pixel[BLUE]/pixel[GREEN])
                self.G_Ratio.append(self.RG_Ratio[index] + self.BG_Ratio[index])
            else:                                               #Set NULLS as None
                self.RG_Ratio.append(0)
                self.BG_Ratio.append(0) 
                self.G_Ratio.append(0)

            if pixel[BLUE] != 0:                             #will avoid NULLS
                self.RB_Ratio.append(pixel[RED]/pixel[BLUE])
                self.GB_Ratio.append(pixel[GREEN]/pixel[BLUE])
                self.B_Ratio.append(self.RB_Ratio[index] + self.GB_Ratio[index])
            else:                                               #Set NULLS as None
                self.RB_Ratio.append(0)
                self.GB_Ratio.append(0)
                self.B_Ratio.append(0)
            
        self.ratios = [self.R_Ratio, self.G_Ratio, self.B_Ratio]
        #print(self.RB_Ratio)
                         
    def pixels_to_image(self, pixel_list, save_name):
        valid_values = [p for p in pixel_list if p is not None]

        if not valid_values:
            print("No valid pixel data to create image")

        # Find min and max to normalize
        min_val = min(valid_values)
        max_val = max(valid_values)
        avg_val = sum(valid_values)/len(valid_values)
        #print(f"min_value = {min_val}")
        #print(f"max_value = {max_val}")

        def normalize(value):
            # Normalize ratio to 0-255
            if value is None:
                return 0 
            if max_val == min_val:
                return 0
            norm = int(255 * (value - min_val) / (max_val - min_val))
            if value >= avg_val:
                norm = 255
            else: 
                norm = 0
            return max(0, min(255, norm))
        
        self.BWpixels = [ (normalize(p), normalize(p), normalize(p)) for p in pixel_list]
        
        new_img = Image.new("RGB", (self.width, self.height))
        new_img.putdata(self.BWpixels)
        self.save_as_jpg(save_name, new_img)

    def blur_image(self, pixel_list, blur_amount = 0):                  #Use black and white pixel list (for now)
        self.blurred_pixels = []
        
        for current_height in range(0, self.height): #check parameter (width)
            for current_width in range(0, self.width): #check parameter (height)
                total_value = 0
                count = 0
                for check_range_height in range(-blur_amount, blur_amount + 1): #check parameter (width)
                    for check_range_width in range(-blur_amount, blur_amount + 1): #check parameter (height)
                        x = current_width + check_range_width
                        y = current_height + check_range_height
                        if 0 <= x < self.width and 0 <= y < self.height:  # bounds check                 
                            index = y * (self.width)+ x
                            total_value += pixel_list[index][0]
                            count += 1
                            
                if count > 0:
                    Average = total_value // count
                else:
                    Average = 0

                self.blurred_pixels.append((Average,Average,Average))
                

        #print(self.refined_pixels)
        new_img = Image.new("RGB", (self.width, self.height))
        new_img.putdata(self.blurred_pixels)
        self.save_as_jpg("Blurred", new_img)
                    
    def refine_area(self, pixel_list, area_check = 0, tolerance = 0.5):                  #Use black and white pixel list (for now)
        self.refined_pixels = []
        
        for current_height in range(0, self.height): #check parameter (height)
            for current_width in range(0, self.width): #check parameter (width)
                total_value = 0
                white_count = 0
                count = 0
                for check_range_height in range(-area_check, area_check + 1): #check parameter (height)
                    for check_range_width in range(-area_check, area_check + 1): #check parameter (width)
                        x = current_width + check_range_width
                        y = current_height + check_range_height
                        if 0 <= x < self.width and 0 <= y < self.height:  # bounds check
                            
                            index = y * (self.width)+ x
                            
                            #print(f"index {index}")
                            total_value = pixel_list[index]
                            if total_value == 0:
                                white_count += 1
                            

                            count += 1
                            #print(f"Average = {Average}")
                
                #print(f"Average = {Average}")
                if count > 0:
                    if white_count <= count * tolerance:
                        total_value = 255
                    else: 
                        total_value = 0
                else:
                    total_value = 0


                self.refined_pixels.append((total_value, total_value, total_value))
                    

        #print(self.refined_pixels)
        new_img = Image.new("RGB", (self.width, self.height))
        new_img.putdata(self.refined_pixels)
        self.save_as_jpg("Refined", new_img)

# region Greyscale functions
 
    def convert_to_grayscale(self, image = None):
        if image is None:
            image = self.image
        self.grayscale_image = image.convert('L')
        self.grayscale_pixel_data = list(self.grayscale_image.getdata())
        self.save_as_jpg("GreyScale", self.grayscale_image)
            
    def grayscale_convert_to_bw(self, alpha = 0.5):
        self.BW_pixel_data = []
        for index in range(0,len(self.grayscale_pixel_data)):
            if self.grayscale_pixel_data[index] >= 255*alpha:
                self.BW_pixel_data.append(255)
            else:
                self.BW_pixel_data.append(0)

        new_img = Image.new('L', (self.width, self.height))
        new_img.putdata(self.BW_pixel_data)
        save_base_path = os.path.join(self.save_base_folder,"BW_image.jpg")
        
        new_img.save(save_base_path)

    def find_edge(self, pixel_list):
        self.edge_pixels = []
        self.edge = []
        for current_height in range(0, self.height): #check parameter (height)
            for current_width in range(0, self.width): #check parameter (width)
                global_index = current_height * (self.width) + current_width
                total_value = 0
                same_as_parent_count = 0
                count = 0
                for check_range_height in range(-1, 1): #check parameter (height)
                    for check_range_width in range(-1, 1): #check parameter (width)
                        x = current_width + check_range_width
                        y = current_height + check_range_height
                        if 0 <= x < self.width and 0 <= y < self.height:  # bounds check
                            count += 1
                            index = y * (self.width) + x
                            value = pixel_list[index]
                            if value == pixel_list[global_index]:
                                same_as_parent_count += 1
                
                if same_as_parent_count in range(4,6):
                    total_value = 255
                else: 
                    total_value = 0
                self.edge.append((255, total_value,total_value ))        
        
        new_img = Image.new("RGB", (self.width, self.height))
        new_img.putdata(self.edge)
        self.save_as_jpg("Edge_pixels", new_img)        


# end region                                     


    def save_as_jpg(self, save_name, image = None):
        try:
            if not save_name.lower().endswith('.jpg'):
                save_name += '.jpg'
            save_base_path = os.path.join(self.save_base_folder,save_name)
            image.save(save_base_path, "JPEG")

            print(f"Image saved as JPEG to {save_base_path}")
        except Exception as e:
            print(f"An error has occured: {e}")


        
if __name__ == "__main__":
    image = ImageProcessor(r"MyApp\Apps\Object_Detection\Images\Couch.jpg")