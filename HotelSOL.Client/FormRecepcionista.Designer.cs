// FormRecepcionista.Designer.cs
using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;

namespace HotelSOL.Client
{
    partial class FormRecepcionista
    {
        private IContainer components = null;
        private TabControl tabControl;
        private TabPage tabClientes, tabReservas, tabDisponibilidad, tabFacturas, tabServicios;

        // CLIENTES
        private Label lblNombreCliente, lblApellidoCliente, lblEmailCliente,
                      lblMovilCliente, lblPasswordCliente, lblEsVipCliente;
        private TextBox txtNombreCliente, txtApellidoCliente, txtEmailCliente,
                        txtMovilCliente, txtPasswordCliente;
        private ComboBox cmbEsVip;
        private Button btnCrearCliente, btnActualizarCliente, btnRefrescarClientes;
        private DataGridView dgvClientes;

        // RESERVAS
        private Label lblClienteReserva, lblTipoReserva, lblHabitacionReserva,
                      lblEstadoReserva, lblFechaEntrada, lblFechaSalida;
        private ComboBox cmbClienteId, cmbTipoReserva, cmbHabitacion, cmbEstado;
        private DateTimePicker dtpEntrada, dtpSalida;
        private Button btnCrearReserva, btnModificarReserva, btnAnularReserva;
        private DataGridView dgvReservas;

        // DISPONIBILIDAD
        private Label lblDisponEntrada, lblDisponSalida;
        private DateTimePicker dtpDisponEntrada, dtpDisponSalida;
        private Button btnConsultarDispon;
        private DataGridView dgvDisponibilidad;

        // FACTURACIÓN
        private Label lblClientesFacturaList, lblFacturas, lblDetalleFactura;
        private DataGridView dgvClientesFacturas, dgvFacturas;
        private Button btnCrearFactura, btnImprimirFactura;
        private TextBox txtDetalleFactura;

        // SERVICIOS
        private Label lblReservaServicio, lblServicio;
        private ComboBox cmbReservaServicio, cmbServicios;
        private Button btnSolicitarServicio;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
                components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            components = new Container();
            tabControl = new TabControl();
            tabClientes = new TabPage();
            tabReservas = new TabPage();
            tabDisponibilidad = new TabPage();
            tabFacturas = new TabPage();
            tabServicios = new TabPage();

            // TabControl
            tabControl.Dock = DockStyle.Fill;
            tabControl.Font = new Font("Segoe UI", 10);
            tabControl.Controls.AddRange(new Control[]
            {
                tabClientes, tabReservas, tabDisponibilidad, tabFacturas, tabServicios
            });

            // --- Tab Clientes ---
            lblNombreCliente = new Label() { Text = "Nombre:", Location = new Point(20, 30) };
            txtNombreCliente = new TextBox() { Location = new Point(150, 30), Width = 250 };
            lblApellidoCliente = new Label() { Text = "Apellido:", Location = new Point(20, 70) };
            txtApellidoCliente = new TextBox() { Location = new Point(150, 70), Width = 250 };
            lblEmailCliente = new Label() { Text = "Email:", Location = new Point(20, 110) };
            txtEmailCliente = new TextBox() { Location = new Point(150, 110), Width = 250 };
            lblMovilCliente = new Label() { Text = "Móvil:", Location = new Point(20, 150) };
            txtMovilCliente = new TextBox() { Location = new Point(150, 150), Width = 250 };
            lblPasswordCliente = new Label() { Text = "Contraseña:", Location = new Point(20, 190) };
            txtPasswordCliente = new TextBox() { Location = new Point(150, 190), Width = 250, UseSystemPasswordChar = true };
            lblEsVipCliente = new Label() { Text = "¿Es VIP?", Location = new Point(20, 230) };
            cmbEsVip = new ComboBox() { Location = new Point(150, 230), Width = 250, DropDownStyle = ComboBoxStyle.DropDownList };
            cmbEsVip.Items.AddRange(new object[] { "Sí", "No" });
            btnCrearCliente = new Button() { Text = "Crear Cliente", Location = new Point(50, 280), Width = 150 };
            btnActualizarCliente = new Button() { Text = "Actualizar Cliente", Location = new Point(220, 280), Width = 180 };
            btnRefrescarClientes = new Button() { Text = "Refrescar", Location = new Point(420, 280), Width = 120 };
            dgvClientes = new DataGridView()
            {
                Location = new Point(20, 330),
                Size = new Size(740, 200),
                ReadOnly = true,
                SelectionMode = DataGridViewSelectionMode.FullRowSelect,
                AutoGenerateColumns = true
            };
            tabClientes.Text = "Clientes";
            tabClientes.Controls.AddRange(new Control[]
            {
                lblNombreCliente, txtNombreCliente,
                lblApellidoCliente, txtApellidoCliente,
                lblEmailCliente, txtEmailCliente,
                lblMovilCliente, txtMovilCliente,
                lblPasswordCliente, txtPasswordCliente,
                lblEsVipCliente, cmbEsVip,
                btnCrearCliente, btnActualizarCliente, btnRefrescarClientes,
                dgvClientes
            });

            // --- Tab Reservas ---
            lblClienteReserva = new Label() { Text = "Cliente:", Location = new Point(20, 30) };
            cmbClienteId = new ComboBox() { Location = new Point(150, 30), Width = 250, DropDownStyle = ComboBoxStyle.DropDownList };
            lblTipoReserva = new Label() { Text = "Tipo Reserva:", Location = new Point(20, 70) };
            cmbTipoReserva = new ComboBox() { Location = new Point(150, 70), Width = 250, DropDownStyle = ComboBoxStyle.DropDownList };
            lblHabitacionReserva = new Label() { Text = "Habitación:", Location = new Point(20, 110) };
            cmbHabitacion = new ComboBox() { Location = new Point(150, 110), Width = 250, DropDownStyle = ComboBoxStyle.DropDownList };
            lblEstadoReserva = new Label() { Text = "Estado:", Location = new Point(20, 150) };
            cmbEstado = new ComboBox() { Location = new Point(150, 150), Width = 250, DropDownStyle = ComboBoxStyle.DropDownList };
            lblFechaEntrada = new Label() { Text = "Fecha Entrada:", Location = new Point(20, 190) };
            dtpEntrada = new DateTimePicker() { Location = new Point(150, 190), Width = 250 };
            lblFechaSalida = new Label() { Text = "Fecha Salida:", Location = new Point(20, 230) };
            dtpSalida = new DateTimePicker() { Location = new Point(150, 230), Width = 250 };
            btnCrearReserva = new Button() { Text = "Crear Reserva", Location = new Point(50, 280), Width = 150 };
            btnModificarReserva = new Button() { Text = "Modificar Reserva", Location = new Point(220, 280), Width = 180 };
            btnAnularReserva = new Button() { Text = "Anular Reserva", Location = new Point(420, 280), Width = 150 };
            dgvReservas = new DataGridView()
            {
                Location = new Point(20, 330),
                Size = new Size(740, 200),
                ReadOnly = true,
                SelectionMode = DataGridViewSelectionMode.FullRowSelect,
                AutoGenerateColumns = false
            };
            tabReservas.Text = "Reservas";
            tabReservas.Controls.AddRange(new Control[]
            {
                lblClienteReserva, cmbClienteId,
                lblTipoReserva, cmbTipoReserva,
                lblHabitacionReserva, cmbHabitacion,
                lblEstadoReserva, cmbEstado,
                lblFechaEntrada, dtpEntrada,
                lblFechaSalida, dtpSalida,
                btnCrearReserva, btnModificarReserva, btnAnularReserva,
                dgvReservas
            });

            // --- Tab Disponibilidad ---
            lblDisponEntrada = new Label() { Text = "Fecha Entrada:", Location = new Point(20, 30) };
            dtpDisponEntrada = new DateTimePicker() { Location = new Point(150, 30), Width = 250 };
            lblDisponSalida = new Label() { Text = "Fecha Salida:", Location = new Point(20, 70) };
            dtpDisponSalida = new DateTimePicker() { Location = new Point(150, 70), Width = 250 };
            btnConsultarDispon = new Button() { Text = "Consultar", Location = new Point(150, 110), Width = 150 };
            dgvDisponibilidad = new DataGridView()
            {
                Location = new Point(20, 160),
                Size = new Size(740, 340),
                ReadOnly = true,
                SelectionMode = DataGridViewSelectionMode.FullRowSelect,
                AutoGenerateColumns = true
            };
            tabDisponibilidad.Text = "Disponibilidad";
            tabDisponibilidad.Controls.AddRange(new Control[]
            {
                lblDisponEntrada, dtpDisponEntrada,
                lblDisponSalida, dtpDisponSalida,
                btnConsultarDispon, dgvDisponibilidad
            });

            // --- Tab Facturación ---
            lblClientesFacturaList = new Label() { Text = "Clientes:", Location = new Point(20, 20) };
            dgvClientesFacturas = new DataGridView()
            {
                Location = new Point(20, 50),
                Size = new Size(740, 150),
                ReadOnly = true,
                SelectionMode = DataGridViewSelectionMode.FullRowSelect,
                AutoGenerateColumns = true
            };
            lblFacturas = new Label() { Text = "Facturas:", Location = new Point(20, 210) };
            dgvFacturas = new DataGridView()
            {
                Location = new Point(20, 240),
                Size = new Size(740, 140),
                ReadOnly = true,
                SelectionMode = DataGridViewSelectionMode.FullRowSelect,
                AutoGenerateColumns = false
            };
            btnCrearFactura = new Button() { Text = "Crear Factura", Location = new Point(20, 390), Width = 150 };
            btnImprimirFactura = new Button() { Text = "Imprimir Factura", Location = new Point(200, 390), Width = 150 };
            lblDetalleFactura = new Label() { Text = "Detalle de Factura:", Location = new Point(20, 430) };
            txtDetalleFactura = new TextBox()
            {
                Location = new Point(20, 460),
                Size = new Size(740, 100),
                Multiline = true,
                ReadOnly = true,
                ScrollBars = ScrollBars.Vertical
            };
            tabFacturas.Text = "Facturación";
            tabFacturas.Controls.AddRange(new Control[]
            {
                lblClientesFacturaList, dgvClientesFacturas,
                lblFacturas, dgvFacturas,
                btnCrearFactura, btnImprimirFactura,
                lblDetalleFactura, txtDetalleFactura
            });

            // --- Tab Servicios ---
            lblReservaServicio = new Label() { Text = "Reserva:", Location = new Point(20, 30) };
            cmbReservaServicio = new ComboBox() { Location = new Point(150, 30), Width = 250, DropDownStyle = ComboBoxStyle.DropDownList };
            lblServicio = new Label() { Text = "Servicio:", Location = new Point(20, 70) };
            cmbServicios = new ComboBox() { Location = new Point(150, 70), Width = 250, DropDownStyle = ComboBoxStyle.DropDownList };
            btnSolicitarServicio = new Button() { Text = "Añadir Servicio", Location = new Point(150, 110), Width = 150 };
            tabServicios.Text = "Servicios";
            tabServicios.Controls.AddRange(new Control[]
            {
                lblReservaServicio, cmbReservaServicio,
                lblServicio, cmbServicios,
                btnSolicitarServicio
            });

            // --- Form Principal ---
            Text = "Panel de Recepcionista";
            ClientSize = new Size(800, 600);
            Controls.Add(tabControl);
        }
    }
}
