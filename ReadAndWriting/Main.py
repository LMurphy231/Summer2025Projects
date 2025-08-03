
from tkinter import *
from tkinter.ttk import *

window = Tk()

def ReadFile():
    with open("TestFile.txt", "r") as f:
        content = f.read()
        print(content)
    return 

def get_user_input():
    """Retrieves the text from the Entry widget and displays it."""
    user_text = entry_field.get()
    if user_text:
        messagebox.showinfo("User Input", f"You entered: {user_text}")
    else:
        messagebox.showwarning("No Input", "Please enter some text.")

def resizeImage(img, newWidth, newHeight):
    oldWidth = img.width()
    oldHeight = img.height()
    newPhotoImage = PhotoImage(width=newWidth, height=newHeight)
    for x in range(newWidth):
        for y in range(newHeight):
            xOld = int(x*oldWidth/newWidth)
            yOld = int(y*oldHeight/newHeight)
            rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
            newPhotoImage.put(rgb, (x, y))
    return newPhotoImage
                              
def open_new_window():
        new_window = Toplevel(window)  # Create a new window
        new_window.title("New Window")
        new_window.geometry("250x150")  
        Label(new_window, text="This is a new window").pack(pady=20)
        Button(new_window, text="Print File", command=print("button clicked")).pack(pady=10)

mouse_x = 0
mouse_y = 0
def get_mouse_position(event):
        global mouse_x 
        global mouse_y
        
        mouse_x = window.winfo_pointerx() - window.winfo_rootx()
        mouse_y = window.winfo_pointery() - window.winfo_rooty()
        #mouse_x = event.x
        #mouse_y = event.y
        print(f"Mouse position: x={mouse_x}, y={mouse_y}")
        
        return  mouse_x, mouse_y
     
def MoveImage():
    axolotllabal.place(x=x,y=y)
     
     

# Create an Entry widget
entry_field = Entry(window, width=40)
entry_field.pack(pady=10, padx=50)

submit_button = Button(window, text="Get Input", command=get_user_input)
submit_button.pack(pady=5,padx=500)

window.bind('<Motion>', get_mouse_position)



# Set the window title (optional)
window.title("My Python Window")

# Set the window size (optional)
window.geometry("1000x500") # width x height

    # Start the Tkinter event loop
    # This keeps the window open and responsive to user interactions
start_x = 0
start_y = 0
def on_drag_start(event):
    global start_x
    global start_y
    start_x = event.x
    start_y = event.y
x = 0
y = 0
def on_drag_motion(event):
    global x
    global y
    x = MoveableImage.winfo_x() + (event.x - start_x)
    y = MoveableImage.winfo_y() + (event.y - start_y)
    MoveableImage.place(x=x, y=y)
    MoveableImage.lift()


Label(window, text="This is the main window").pack(pady=0)
image = resizeImage(PhotoImage(file = r"ReadAndWriting/BogosBinted.png"),100,100)
MoveableImage = Button(window, image = image, command = MoveImage)
MoveableImage.place(x = 10, y = 10)
newimage = Label(window, image = image)

MoveableImage.bind("<ButtonPress-1>", on_drag_start) # Bind left mouse button press
MoveableImage.bind("<B1-Motion>", on_drag_motion)   # Bind mouse motion while left button is pressed

Button(window, text="Open New Window", command=open_new_window).pack(pady=10)
axolotl = resizeImage(PhotoImage(file = r"ReadAndWriting/Axolotl.gif"),400,300)
axolotllabal = Label(window, image = axolotl)
#Button(window, image=image, command=ReadFile).pack(pady=10)
window.mainloop()


def main():
    with open("TestFile.txt", "w") as f:
        f.write("Testing !\n")
        f.write("NEW LINE TEST")

   
        
    with open("TestFile.txt", "r") as f:
        content = f.read()
        print(content)
    print()
    




if __name__ == "__main__":
    main()  