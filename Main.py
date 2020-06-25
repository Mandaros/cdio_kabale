import GUIClass

# 1. boolean - True  - tager ikke input fra CV
#            - False - tager input fra CV
# 2. boolean - True  - Køre på GPU, kræver Nvidia samt CUDA installeret (Høj FPS)
#            - False - Køre på CPU (lav FPS)
gui = GUIClass.GUI(True, False)

gui.tk.mainloop()
