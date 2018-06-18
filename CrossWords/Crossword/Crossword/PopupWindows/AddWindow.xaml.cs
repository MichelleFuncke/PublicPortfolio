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

            cboDirections.ItemsSource = Enum.GetValues(typeof(Direction));
            cboDirections.SelectedIndex = 0;

            udColumn.Maximum = maxCol;
            udRow.Maximum = maxRow;
        }

        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            if (tbxWord.Text.Length > 0)
            {
                int number = 1;
                int.TryParse(tbxNumber.Text, out number);
                Word = new PuzzleWord(tbxWord.Text, number, tbxClue.Text, cboDirections.SelectedValue.ToString(), (int)udColumn.Value - 1, (int)udRow.Value - 1);

                this.DialogResult = true;
                this.Close();
            }
        }
    }
}
