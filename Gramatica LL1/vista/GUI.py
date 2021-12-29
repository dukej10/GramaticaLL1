

import tkinter as tk
from tkinter import messagebox

import modelo.Proceso as Proceso


class VentanaGramatica():

    def __init__(self, datos = []):
        #ventana
        self.backgroung = "#25A18E"
        self.indice = 0
        self.datos = datos
        self.inv = 0
        self.cont = 0
        self.contarGramaticas = 0
        self.cumpleLL1 = []
        ventana = tk.Tk()
        ventana.title("Ventana Estructuras de Lenguajes Gramáticas LL1")
        ventana.state("zoomed")
        ventana.iconphoto(False, tk.PhotoImage(file = "C:/Users/Juandi Duque/Documents/LENGUAJES/Gramatica LL1/Recursos/py.png"))
        ventana.config(bg = self.backgroung)
        ventana.resizable(1, 1)
        
        #Imagenes
        imgLogoU = tk.PhotoImage(file="C:/Users/Juandi Duque/Documents/LENGUAJES/Gramatica LL1/Recursos/LogoU.png")
        imgLogoU = imgLogoU.subsample(11) # para redimensionar imagen
        #Labels
        lblMateria = tk.Label(ventana, text = "Estructura de Lenguajes", bg = self.backgroung,
                 font=("Verdana",18))
        lblMateria.place(x = 10, y = 10)
        logoU = tk.Label(ventana, image = imgLogoU, bg = self.backgroung)
        logoU.place(x = 1230, y = 5)

        titulo = tk.Label(ventana,
                 fg="black",
                 bg=self.backgroung,
                 borderwidth = 10,
                 justify="center",
                 compound = "left",
                 font=("Verdana",24),
                 text="Proyecto Gramáticas LL1")
        titulo.pack(anchor = "center")

        lblGramatica = tk.Label(ventana,
                 fg="black",
                 bg=self.backgroung,
                 text = "Gramática a evaluar",
                 font=("Verdana",12))
        lblGramatica.place(x = 140, y = 130)
        lblFactorizacion  = tk.Label(ventana,
                 fg="black",
                 bg=self.backgroung,
                 text = "Factorización",
                 font=("Verdana",12))
        lblFactorizacion.place(x = 620, y = 130)
        lblRecursion  = tk.Label(ventana,
                 fg="black",
                 bg= self.backgroung,
                 text = "Recursión Izquierda",
                 font=("Verdana",12))
        lblRecursion.place(x = 1070, y = 130)
        lblPrimeros = tk.Label(ventana,
                 fg="black",
                 bg=self.backgroung,
                 text = "Primeros",
                 font=("Verdana",12))
        lblPrimeros.place(x = 185, y = 420)
        lblSiguientes = tk.Label(ventana,
                 fg="black",
                 bg=self.backgroung,
                 text = "Siguientes",
                 font=("Verdana",12))
        lblSiguientes.place(x = 630, y = 420)
        lblPrediccion = tk.Label(ventana,
                 fg="black",
                 bg=self.backgroung,
                 text = "Conjunto Predicción",
                 font=("Verdana",12))
        lblPrediccion.place(x = 1070, y = 420)
        # Sección conteo de grámaticas
        self.contador = tk.Label(ventana,
                 fg="black",
                 bg=self.backgroung,
                 text = "Contador \n  Grámaticas",
                 font=("Verdana",12))
        self.contador.place(x = 925, y = 630)

        self.txtCont = tk.Text(ventana,
                 fg="black",
                bd = 0,
                 bg=self.backgroung,
                 height = 1,
                 width = 1,
                 font=("Verdana",20))
        self.txtCont.place(x=1050, y=630)

        #Botones
        botonAceptar = tk.Button(ventana, 
                                 text ="Aceptar", 
                                 bg = "#004e64",
                                 borderwidth = 3,
                                 fg = "white", 
                                 height = 1, 
                                 relief = "groove",
                                 width = 8,
                                 font=("Verdana",15), 
                                 command = lambda : self.procedimiento())
        botonAceptar.place(x = 320, y = 333)
        self.botonCargar = tk.Button(ventana,
                                 text ="Cargar",
                                 bg = "#004e64",
                                 borderwidth = 3,
                                 fg = "white",
                                 height = 1,
                                 relief = "groove",
                                 width = 8,
                                 font=("Verdana",15),
                                 command = lambda : self.leer())
        self.botonCargar.place(x = 30, y = 333)
        self.botonSiguiente = tk.Button(ventana,
                                        text ="Siguiente",
                                        bg = "#004e64",
                                        borderwidth = 3,
                                        fg = "white",
                                        height = 1,
                                        width = 8,
                                        relief = "groove",
                                        font=("Verdana",15),
                                        command = lambda : self.habilitarSiguiente())
        self.botonSiguiente.place(x=1230, y=630)
        self.botonValidas = tk.Button(ventana,
                                text ="Ver Válidas",
                                bg = "#004e64",
                                borderwidth = 3,
                                fg = "white",
                                height = 1,
                                width = 12,
                                relief = "groove",
                                font=("Verdana",15),
                                command = lambda : self.mostrarValidas(self.cumpleLL1))
        self.botonValidas.place(x=35, y=630)
        
        #Campos de texto
        self.txtGramaticaEntrada = tk.Text(ventana,
                                           fg="black",
                                           bg="white",
                                           height = 9,
                                           width = 40,
                                           font=("Verdana",12))
        self.txtGramaticaEntrada.place(x = 30, y = 160)
        self.txtFactorizacion = tk.Text(ventana,
                                        fg="black",
                                        bg="white",
                                        height = 9,
                                        width = 40,
                                        font=("Verdana",12))
        self.txtFactorizacion.place(x =480, y = 160)
        self.txtRecursion = tk.Text(ventana,
                                    fg="black",
                                    bg="white",
                                    height = 9,
                                    width = 40,
                                    font=("Verdana",12))
        self.txtRecursion.place(x =940, y = 160)
        self.txtPrimeros = tk.Text(ventana,
                                   fg="black",
                                   bg="white",
                                   height = 9,
                                   width = 40,
                                   font=("Verdana",12))
        self.txtPrimeros.place(x = 35, y = 450)
        self.txtSiguientes = tk.Text(ventana,
                                     fg="black",
                                     bg="white",
                                     height = 9,
                                     width = 40,
                                     font=("Verdana",12))
        self.txtSiguientes.place(x = 480, y = 450)
        self.txtConjuntoPrediccion = tk.Text(ventana,
                                             fg="black",
                                             bg="white",
                                             height = 9,
                                             width = 40,
                                             font=("Verdana",12))
        self.txtConjuntoPrediccion.place(x = 940, y = 450)
        self.estadoTexto("Deshabilitar")
        #Apertura de la ventana
        ventana.mainloop()

    def leer(self):
        # print(len(self.datos))
        # Para solo cargar una gramatica
        self.txtGramaticaEntrada.configure(state='normal')  # Habilitar que se pueda editar
        if self.inv == 0 and self.indice < len(self.datos):
            self.inv = 1
            self.txtGramaticaEntrada.insert(1.0, self.datos[self.indice])
            self.txtGramaticaEntrada.configure(state='disabled') # Deshabilitar que se pueda editar
            self.botonCargar.configure(state = 'disabled')

    def procedimiento(self):
        T = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # NO TERMINALES
        self.estadoTexto("Habilitar")
        if self.cont == 0: # Para no ecribir varias veces el mismo texto al dar click en Aceptar
            self.cont = 1
            try:
                gramatica = Proceso.convertirLibreContexto(self.txtGramaticaEntrada.get("1.0", "end-1c"), 'λ')
                gramaticaFactorComun = Proceso.eliminarFactorizacionIzquierda(gramatica)
                self.txtFactorizacion.insert(1.0, gramaticaFactorComun)
                gramaticaRecursion = Proceso.eliminarRecursionIzquierda(gramaticaFactorComun)
                self.txtRecursion.insert(1.0, gramaticaRecursion)
                resultadoPrimeros = ""
                for noTerminal in gramaticaRecursion.noTerminales:
                    # print(noTerminal)
                    tempLstPrimeros = gramaticaRecursion.primeros(noTerminal)
                    tmp = ""
                    # print(" P", tempLstPrimeros)
                    for i in range(len(tempLstPrimeros)):
                      if tempLstPrimeros[i] not in T:
                        tmp += tempLstPrimeros[i]
                        # print("P ", tmp)
                        if (i < len(tempLstPrimeros) - 1):
                            tmp += ", "
                    resultadoPrimeros += "Prim(" + noTerminal + ") = { " + tmp + " } \n"
                self.txtPrimeros.insert(1.0, resultadoPrimeros)

                resultadoSiguientes = ""
                for noTerminal in gramaticaRecursion.noTerminales:
                    tempLstSiguientes = gramaticaRecursion.siguientes(noTerminal)
                    tmp = ""
                    for j in range(len(tempLstSiguientes)):
                        if tempLstSiguientes[j] not in T:
                            tmp += tempLstSiguientes[j]
                            if (j < len(tempLstSiguientes) - 1):
                                tmp += ", "
                    resultadoSiguientes += "Sig(" + noTerminal + ") = { " + tmp + " } \n"
                self.txtSiguientes.insert(1.0, resultadoSiguientes)

                conjuntoPrediccion = ""
                tieneInterseccion = False
                producciones = gramaticaRecursion.__str__()
                lstProducciones= producciones.split("\n")
                for prod in lstProducciones:
                    if (prod.find("|") == -1):
                        lstTemp = prod.split("->")
                        tmp = ""
                        lstCp = gramaticaRecursion.conjuntoPrediccion(lstTemp[0], lstTemp[1])
                        for i in range(len(lstCp)):
                            if lstCp[i] not in T:
                                tmp += lstCp[i]
                                if(i < len(lstCp) - 1):
                                    tmp += ", "
                        conjuntoPrediccion += "CP(" + prod + ") = { " + tmp + " } \n"
                    else:
                        lstTemp = prod.split("->")
                        lstTemp2 = lstTemp[1].split("|")
                        lstInter = []
                        for j in range(len(lstTemp2)):
                            lstCp = gramaticaRecursion.conjuntoPrediccion(lstTemp[0], lstTemp2[j])
                            tmp = ""
                            for k in range(len(lstCp)):
                                lstInter.append(lstCp[k])
                                if lstCp[k] not in T:
                                    tmp += lstCp[k]
                                    if (k < len(lstCp) - 1):
                                        tmp += ", "
                            conjuntoPrediccion += "CP(" + lstTemp[0] + " -> " + lstTemp2[j] + ") = { " + tmp + " } \n"
                        if (gramaticaRecursion.hayInterseccion(lstInter)):
                            tieneInterseccion = True
                self.txtConjuntoPrediccion.insert(1.0, conjuntoPrediccion)
                if (tieneInterseccion):
                    messagebox.showinfo(title = "Mensaje", message = "La gramática no es LL1")

                else:
                    messagebox.showinfo(title = "Mensaje", message = "La gramática es LL1")
                    self.cumpleLL1.append(gramatica) # Almacena las gramáticas que cumplen
                self.contarGramaticas = self.contarGramaticas + 1
                self.conteoGramaticas()
            except:
                messagebox.showinfo(title = "Mensaje", message = "Gramática Inválida")
            self.estadoTexto("Deshabilitar")

    def mostrarValidas(self, gramaticaCumple):
        if len(gramaticaCumple) > 0:
            for i in range(len(self.cumpleLL1)):
                messagebox.showinfo(title=str(i + 1), message=self.cumpleLL1[i])
        else:
            messagebox.showinfo(title="Mensaje", message="Todavía no se ingresa \n una gramática LL1")

    def habilitarSiguiente(self):
        self.estadoTexto("Habilitar")
        self.txtConjuntoPrediccion.delete("1.0", "end")
        self.txtSiguientes.delete("1.0", "end")
        self.txtPrimeros.delete("1.0", "end")
        self.txtFactorizacion.delete("1.0", "end")
        self.txtRecursion.delete("1.0", "end")
        self.txtGramaticaEntrada.delete("1.0", "end")
        self.txtCont.delete("1.0", "end")
        self.inv = 0 # Solo cargar una gramatica
        self.indice = self.indice + 1
        self.botonCargar.configure(state = 'normal')
        # Se deshabilita cuando no hay mas gramaticas que mostrar
        if self.indice == len(self.datos)-1:
            self.botonSiguiente.configure(state ='disabled')
        self.cont = 0

    def conteoGramaticas(self):
        self.txtCont.configure(state = 'normal')
        self.txtCont.insert(1.0, str(self.contarGramaticas))
        self.txtCont.configure(state='disable')

    def estadoTexto(self, estado):
        if estado == "Habilitar":
            self.txtGramaticaEntrada.configure(state='normal')  # Habilitar que se pueda editar
            self.txtConjuntoPrediccion.configure(state='normal')
            self.txtSiguientes.configure(state='normal')
            self.txtPrimeros.configure(state='normal')
            self.txtFactorizacion.configure(state='normal')
            self.txtRecursion.configure(state='normal')
        else:
            self.txtGramaticaEntrada.configure(state='disabled')  # Deshabilitar que se pueda editar
            self.txtConjuntoPrediccion.configure(state='disabled')
            self.txtSiguientes.configure(state='disabled')
            self.txtPrimeros.configure(state='disabled')
            self.txtFactorizacion.configure(state='disabled')
            self.txtRecursion.configure(state='disabled')