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
    /// Interaction logic for EditWindow.xaml
    /// </summary>
    public partial class EditWindow : Window
    {
        public PuzzleWord Word { get; set; }

        public EditWindow(PuzzleWord theWord, int maxCol, int maxRow)
        {
            InitializeComponent();
            Word = theWord.Copy();
            WindowSetup();

            udColumn.Maximum = maxCol - 1;
            udRow.Maximum = maxRow - 1;

            cboDirections.ItemsSource = Enum.GetValues(typeof(Direction));
        }

        private void WindowSetup()
        {
            InitializeComponent();
            this.DataContext = Word;

            Application curApp = Application.Current;
            Window mainWindow = curApp.MainWindow;
            this.Left = mainWindow.Left + (mainWindow.Width - this.Width) / 2;
            this.Top = mainWindow.Top + (mainWindow.Height - this.Height) / 2;
        }

        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            this.DialogResult = true;
            this.Close();
        }
    }
}
