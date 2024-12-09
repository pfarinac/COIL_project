from PyQt6.QtWidgets import (QWidget,
                             QVBoxLayout, QMainWindow, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from frontend.data_UI import UI
from frontend.prepro_UI import PUI
from frontend.model_UI import MUI
from frontend.SLD_UI import SLDUI


class CsvViewer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.df = None  # DataFrame para almacenar el archivo cargado

        self.inicializarUI()

    def inicializarUI(self):

        self.setWindowTitle("CSV/XLSX/SQLite Viewer")
        self.setGeometry(100, 100, 1920, 1080)

        self.d_u = UI()
        self.p_u = PUI(self.d_u.d_f)
        self.m_u = MUI(self.d_u.d_f)
        self.sld_u = SLDUI(self.m_u.funcs)
        self.d_u.confirm.clicked.connect(self.habilitar_count_nulls)
        self.p_u.btn_count_nulls.clicked.connect(self.habilitar_model_button)

        self.m_u.model_button.clicked.connect(self.deshabilitar_buttons)
        self.m_u.model_button.clicked.connect(
            self.sld_u.funcs.reset_input_fields)
        self.m_u.model_button.clicked.connect(self.enable_model)

        self.d_u.load_model_button.clicked.connect(self.sld_u.funcs.load_model)

        self.d_u.load_model_button.clicked.connect(self.display_loaded_model)
        self.d_u.load_model_button.clicked.connect(
            self.sld_u.enable_prediction)

        self.p_u.layout_entrada_salida_preprocesado.addLayout(
            self.d_u.layout_entrada_salida)
        self.p_u.layout_entrada_salida_preprocesado.addLayout(
            self.p_u.layout_preprocesado)
        self.p_u.layout_entrada_salida_preprocesado.setAlignment(
            Qt.AlignmentFlag.AlignCenter)

        self.m_u.layout_visualizar_iniciar_modelo.addLayout(
            self.sld_u.layout_descripcion_modelo)

        # Creamos el layout principal y le añadimos los auxiliares
        layout = QVBoxLayout()
        layout.addLayout(self.d_u.layout)
        layout.addLayout(self.p_u.layout_entrada_salida_preprocesado)
        layout.addLayout(self.m_u.layout_visualizar_iniciar_modelo)
        layout.addLayout(self.sld_u.description_layout)
        layout.addLayout(self.sld_u.layout_mostrar_prediccion)
        layout.addLayout(self.sld_u.layout_guardarmodelo_prediccion)

        container = QWidget()
        container.setLayout(layout)

        # Crear un área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Desactiva el scroll horizontal
        # Activa el scroll vertical solo si es necesario
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Crear el diseño principal y añadir el área de scroll
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(scroll_area)

        # Configurar el diseño principal para la ventana
        self.setCentralWidget(main_widget)

    def habilitar_count_nulls(self):
        self.p_u.btn_count_nulls.setEnabled(True)

    def habilitar_model_button(self):
        self.m_u.model_button.setEnabled(True)

    def deshabilitar_buttons(self):
        self.p_u.btn_count_nulls.setEnabled(False)
        self.p_u.btn_remove_nulls.setEnabled(False)
        self.p_u.btn_replace_nulls_mean.setEnabled(False)
        self.p_u.btn_replace_nulls_median.setEnabled(False)
        self.p_u.btn_replace_nulls_value.setEnabled(False)
        self.m_u.model_button.setEnabled(False)

    def display_loaded_model(self):
        if self.sld_u.funcs.file_name:
            # Ocultar secciones de carga de datos y selección de columnas
            self.d_u.table_widget.deleteLater()
            self.d_u.features_label.deleteLater()
            self.d_u.features_list.deleteLater()
            self.d_u.target_label.deleteLater()
            self.d_u.target_combo.deleteLater()
            self.d_u.viewer_title.deleteLater()
            self.p_u.prep_title.deleteLater()
            self.m_u.model_title.deleteLater()
            self.d_u.entrada_salida_titulo.deleteLater()
            # Botones de preprocesado
            self.p_u.btn_count_nulls.deleteLater()
            self.p_u.btn_remove_nulls.deleteLater()
            self.p_u.btn_replace_nulls_mean.deleteLater()
            self.p_u.btn_replace_nulls_median.deleteLater()
            self.p_u.btn_replace_nulls_value.deleteLater()
            self.d_u.confirm.deleteLater()
            self.m_u.model_button.deleteLater()
            self.d_u.load_button.deleteLater()
            self.d_u.file_path_label.deleteLater()
            self.sld_u.save_button.setEnabled(True)
            # Modelo
            self.m_u.canvas.deleteLater()
            self.m_u.graph_widget.deleteLater()
            self.m_u.label_formula.setVisible(True)
            self.m_u.label_r2_mse.setVisible(True)
            self.sld_u.result_label.setVisible(False)
            # Mostrar los detalles del modelo cargado
            if "model" in self.sld_u.funcs.loaded_model_data:
                # Actualizar etiquetas
                self.m_u.label_formula.setText(
                    f"Model formula: {self.m_u.funcs.formula(self.sld_u.funcs.model_input,self.sld_u.funcs.model_output)}")
                self.m_u.label_r2_mse.setText(
                    f"R²: {self.sld_u.funcs.r2_score}  |  MSE: {self.sld_u.funcs.mse}")
                self.sld_u.description_text.setText(
                    self.sld_u.funcs.description)

    def enable_model(self):
        self.sld_u.save_button.setEnabled(True)
        self.sld_u.predict_button.setEnabled(True)
        self.sld_u.enable_prediction(True)
        QMessageBox.information(
            None, "Model created succesfully", "Your model has been created succesfully")
        if self.sld_u.description_text.toPlainText() == "":
            QMessageBox.information(
                None, "No description", "You haven't assigned any description to the model")
