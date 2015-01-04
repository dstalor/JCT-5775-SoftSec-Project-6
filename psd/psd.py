from psd_Project import psd_Project



class psd:
    def __init__(self):
        self.psd_project = None

    def create_new_project(self, filename = None):
        self.psd_project = psd_Project(self, filename)



if __name__=="__main__":
    psd_main = psd()
    psd_main.create_new_project("examples\\helloworld.exe")

    psd_main.psd_project.pe.print_info()


