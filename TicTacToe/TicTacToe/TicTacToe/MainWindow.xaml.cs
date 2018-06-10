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

namespace TicTacToe
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public Board theBoard;
        public MainWindow()
        {
            InitializeComponent();

            theBoard = new Board();
        }

        private void btn_topleft_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(0, 0);
            btn_topleft.Content = FindResource(theBoard.Grid[0, 0].ToString());
        }

        private void btn_topcentre_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(0, 1);
            btn_topcentre.Content = FindResource(theBoard.Grid[0, 1].ToString());
        }

        private void btn_topright_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(0, 2);
            btn_topright.Content = FindResource(theBoard.Grid[0, 2].ToString());
        }

        private void btn_left_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(1, 0);
            btn_left.Content = FindResource(theBoard.Grid[1, 0].ToString());
        }

        private void btn_centre_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(1, 1);
            btn_centre.Content = FindResource(theBoard.Grid[1, 1].ToString());
        }

        private void btn_right_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(1, 2);
            btn_right.Content = FindResource(theBoard.Grid[1, 2].ToString());
        }

        private void btn_bottomleft_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(2, 0);
            btn_bottomleft.Content = FindResource(theBoard.Grid[2, 0].ToString());
        }

        private void btn_bottomcentre_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(2, 1);
            btn_bottomcentre.Content = FindResource(theBoard.Grid[2, 1].ToString());
        }

        private void btn_bottomright_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(2, 2);
            btn_bottomright.Content = FindResource(theBoard.Grid[2, 2].ToString());
        }
    }
}
