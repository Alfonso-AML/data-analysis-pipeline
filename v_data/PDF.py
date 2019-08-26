from fpdf import FPDF

class PDF(FPDF):

     def new_page(self, titulo):  
        self.add_page()                            
        self.set_font('Arial', 'B', 15)            # fuente Arial negrita 15  
        ancho=self.get_string_width(titulo)+6      # calcula el ancho del titulo y su posicion
        self.set_x((210-ancho)/2)
        self.set_draw_color(0, 80, 180)            # colores del marco, fondo y texto
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        self.set_line_width(1)                     # ancho del marco (1 mm)
        self.cell(ancho, 9, titulo, 1, 1, 'C', 1)  # titulo
        self.ln(10)   

     def print_film(self, film, numero):                      # cuerpo del capitulo
        self.set_font('Times', '', 12)                           # fuente Times 12
        self.cell(0, 5, 'Title and publication year: {} ({})'.format(film['title'],film['year']))
        self.ln()
        if(film['duration']!=' '):
            self.cell(0, 5, 'Duration and average score: {} min / {}'.format(film['duration'], film['average']))
        else:
            self.cell(0, 5, 'Average score: {}'.format(film['average']))
        self.ln()
        self.cell(0, 5, 'Type: {}'.format(film['type']))
        self.ln()
        self.ln()
        self.set_font('Times', 'B', 12) 
        self.cell(0, 5, 'Synopsis')
        self.ln()
        self.set_font('Times', '', 12) 
        self.multi_cell(0, 5, film['synopsis'])                             # texto con saltos de linea (multicelda)
        self.ln()                                        # salto de linea

        try:

            self.image('./posters/%s.jpg' % (film['id']))# imagen 
        except:
            self.image('./posters/not_available.jpg')


        # {'id': request, 
        #                     'title': film_data[0][2],
        #                     'synopsis': synopsis, 
        #                     'poster': film_info['Poster'],
        #                     'averange': average,
        #                     'year': film_data[0][3],
        #                     'duration': film_data[0][4],
        #                     'type': film_data[0][5]
        #                     }