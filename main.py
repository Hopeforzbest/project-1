from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
import fitz  # PyMuPDF

def get_pdf_text(pdf_path):
    all_text = ""
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        all_text += f"Page {page_num + 1}:\n{text}\n\n"
    doc.close()
    return all_text

class PDFTextViewerApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        
        # File chooser
        self.file_chooser = FileChooserListView(filters=['*.pdf'], size_hint=(1, 0.8))
        self.root.add_widget(self.file_chooser)
        
        # Open button
        open_button = Button(text="Open PDF", size_hint=(1, 0.1))
        open_button.bind(on_press=self.open_pdf)
        self.root.add_widget(open_button)
        
        return self.root

    def open_pdf(self, instance):
        selected = self.file_chooser.selection
        if selected:
            pdf_path = selected[0]
            pdf_text = get_pdf_text(pdf_path)
            
            # Create a ScrollView
            scroll_view = ScrollView(size_hint=(1, 0.9))
            
            # Create a Label to display the PDF text
            label = Label(text=pdf_text, font_size='20sp', size_hint_y=None, valign='top', text_size=(self.root.width, None))
            
            # Making sure the label is big enough to contain all the text
            label.bind(width=lambda *x: label.setter('text_size')(label, (label.width, None)),
                       texture_size=lambda *x: setattr(label, 'height', label.texture_size[1]))
            
            # Adding the label to the ScrollView
            scroll_view.add_widget(label)
            
            # Update the root widget to show the PDF text
            self.root.clear_widgets()
            self.root.add_widget(scroll_view)

if __name__ == '__main__':
    PDFTextViewerApp().run()
