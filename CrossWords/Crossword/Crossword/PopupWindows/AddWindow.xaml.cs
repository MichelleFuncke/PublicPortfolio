using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace Crossword.PopupWindows
{
    /// <summary>
    /// Interaction logic for AddWindow.xaml
    /// </summary>
    public partial class AddWindow : Window
    {
        public PuzzleWord Word { get; private set; }

        public AddWindow(int maxCol, int maxRow)
        {
            InitializeComponent();
            WindowSetup();

            cboDirections.ItemsSource = Enum.GetValues(typeof(Direction));
            cboDirections.SelectedIndex = 0;

            udColumn.Maximum = maxCol - 1;
            udRow.Maximum = maxRow - 1;
        }

        private void WindowSetup()
        {
            InitializeComponent();

            Application curApp = Application.Current;
            Window mainWindow = curApp.MainWindow;
            this.Left = mainWindow.Left + (mainWindow.Width - this.Width) / 2;
            this.Top = mainWindow.Top + (mainWindow.Height - this.Height) / 2;

            tbxWord.Focus();
        }

        private void Save()
        {
            if (tbxWord.Text.Length > 0)
            {
                int number = 1;
                int.TryParse(tbxNumber.Text, out number);
                Word = new PuzzleWord(tbxWord.Text, number, tbxClue.Text, cboDirections.SelectedValue.ToString(), (int)udColumn.Value, (int)udRow.Value);

                this.DialogResult = true;
                this.Close();
            }
        }

        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            Save();
        }

        private void winAdd_KeyDown(object sender, KeyEventArgs e)
        {
            if ((e.Key == Key.Return))
            {
                Save();
            }
        }
    }
}
