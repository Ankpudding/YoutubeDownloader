import customtkinter
import time
from pytube import YouTube

customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue") 
app = customtkinter.CTk() 
app.resizable(True, False)
app.geometry("500x365")
app.title("Youtube Downloader")

def download_mp4():
    finishLabel.configure(text="Downloading...", text_color="white")
    print(urlInput.get())
    ytlink = urlInput.get()
    ytObject = YouTube(ytlink, on_progress_callback=on_progress)
        
    if not optionmenu.get() == "Highest Resolution":
        video = ytObject.streams.filter(res=optionmenu.get()).first()
    else:
        video = ytObject.streams.get_highest_resolution()
        
    title.configure(text=ytObject.title, text_color="white")
        
    video.download("C:\\Downloaded Videos")
    print("Download Completed!")
        
    finishLabel.configure(text="Download Completed!  File saved in \"C:\\Downloaded Videos\"", text_color="white")
    app.geometry("500x435")
    
def download_mp3():
    finishLabel.configure(text="Downloading...", text_color="white")
    print(urlInput.get())
    ytlink = urlInput.get()
    ytObject = YouTube(ytlink, on_progress_callback=on_progress)
        
    video = ytObject.streams.filter(abr=optionmenu.get()).first()
        
    title.configure(text=ytObject.title, text_color="white")
        
    video.download("C:\\Downloaded Audios")
    print("Download Completed!")
        
    finishLabel.configure(text="Download Completed!  File saved in \"C:\\Downloaded Audios\"", text_color="white")
    app.geometry("500x435")

def download():
    try:
        if downloadType.get() == "Video":
            download_mp4()
        if downloadType.get() == "Audio":
            download_mp3()
    except Exception as e:
            finishLabel.configure(text=(e),text_color="red")
            print("Link is invalid!",e)
            app.geometry("500x435")
        
def res_function():
    button.configure(text="Download "+downloadType.get())
    try:
        if downloadType.get() == "Video":
            print(urlInput.get())
            ytlink = urlInput.get()
            ytObject = YouTube(ytlink)
            res = []
            print(ytObject.streams)
            for i in ytObject.streams.filter(progressive=True): 
                if i.resolution!=None and i.resolution not in res:
                    res.append(i.resolution)
            res.append("Highest Resolution")
            optionmenu.configure(values=res)
            optionmenu.update()
            optionmenu.set(res[len(res)-1])
            app.geometry("500x595")
        elif downloadType.get() == "Audio":
            print(urlInput.get())
            ytlink = urlInput.get()
            ytObject = YouTube(ytlink)
            res = []
            for i in ytObject.streams.filter(only_audio=True):
                if i.abr!=None and i.abr not in res:
                    res.append(i.abr)
            optionmenu.configure(values=res)
            optionmenu.update()
            optionmenu.set(res[len(res)-1])
            app.geometry("500x595")
    except Exception as e:
        print(e)
    
 
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    rounded_percentage = round(percentage_of_completion, 2)
    progressBar.set(bytes_downloaded / total_size)
    progress.configure(text=f"{rounded_percentage}%")
    progress.update()
    progressBar.update()
    print(f"{rounded_percentage}%")
    


title = customtkinter.CTkLabel(app, text="Paste a Youtube link to download")
title.pack(pady=15)

urlInput = customtkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=35, textvariable=urlInput)
link.pack(pady=15)

def optionmenu_callback(choice):
    pass

text2 = customtkinter.CTkLabel(app, text="Choose download quality")
text2.pack()

optionmenu = customtkinter.CTkOptionMenu(app, values=[""],command=optionmenu_callback)
optionmenu.set("")
optionmenu.pack(pady=15)

text1 = customtkinter.CTkLabel(app, text="Choose file type")
text1.pack()

downloadType = customtkinter.CTkOptionMenu(app, values=["Audio", "Video"])
downloadType.set("Video")
downloadType.pack(pady=15)

button = customtkinter.CTkButton(master=app, text="Update Quality", command=res_function, fg_color="green", border_width=0, text_color=("gray10", "#DCE4EE"), hover_color="darkgreen")
button.pack(pady=15)

finishLabel = customtkinter.CTkLabel(app, text="Waiting for download...")
finishLabel.pack(pady=25)

progress = customtkinter.CTkLabel(app, text="0%")
progress.pack(pady=15)

progressBar = customtkinter.CTkProgressBar(app, orientation="horizontal", width=400)
progressBar.set(0)
progressBar.pack(pady=15)

button = customtkinter.CTkButton(master=app, text="Download "+downloadType.get(), command=download)
button.pack(pady=15)

app.mainloop()