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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Crossword
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void CreateGrid(Panel ParentControl, int ColumnCount, int RowCount, int Size)
        {
            Grid CrossWordGrid = new Grid();
            CrossWordGrid.Background = new SolidColorBrush(Colors.Black);

            for (int i = 0; i < ColumnCount; i++)
            {
                ColumnDefinition Col = new ColumnDefinition();
                Col.Width = new GridLength(Size);

                CrossWordGrid.ColumnDefinitions.Add(Col);
            }

            for (int i = 0; i < RowCount; i++)
            {
                RowDefinition Row = new RowDefinition();
                Row.Height = new GridLength(Size);

                CrossWordGrid.RowDefinitions.Add(Row);
            }

            CrossWordGrid.ShowGridLines = true;

            ParentControl.Children.Add(CrossWordGrid);
        }

        private void mnuLoad_Click(object sender, RoutedEventArgs e)
        {

            CreateGrid(spMainPage, 10, 10, 50);
        }
    }
}
