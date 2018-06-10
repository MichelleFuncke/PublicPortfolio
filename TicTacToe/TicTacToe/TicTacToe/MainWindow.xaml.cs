using System;
using System.Collections.Generic;
using System.Globalization;
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
        
        public Image ConvertMarker(Marker marker)
        {
            Image theImage = new Image()
            {
                HorizontalAlignment = System.Windows.HorizontalAlignment.Center,
                VerticalAlignment = System.Windows.VerticalAlignment.Center,
                Source = new BitmapImage(new Uri("pack://application:,,,/Pictures/" + Enum.GetName(typeof(Marker), marker) + ".png")),
            };
            return theImage;
        }

        public MainWindow()
        {
            InitializeComponent();

            theBoard = new Board();
        }

        private void btn_topleft_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(0, 0);            
            btn_topleft.Content = ConvertMarker(theBoard.Grid[0, 0]);
        }

        private void btn_topcentre_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(0, 1);
            btn_topcentre.Content = ConvertMarker(theBoard.Grid[0, 1]);
        }

        private void btn_topright_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(0, 2);
            btn_topright.Content = ConvertMarker(theBoard.Grid[0, 2]);
        }

        private void btn_left_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(1, 0);
            btn_left.Content = ConvertMarker(theBoard.Grid[1, 0]);
        }

        private void btn_centre_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(1, 1);
            btn_centre.Content = ConvertMarker(theBoard.Grid[1, 1]);
        }

        private void btn_right_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(1, 2);
            btn_right.Content = ConvertMarker(theBoard.Grid[1, 2]);
        }

        private void btn_bottomleft_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(2, 0);
            btn_bottomleft.Content = ConvertMarker(theBoard.Grid[2, 0]);
        }

        private void btn_bottomcentre_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(2, 1);
            btn_bottomcentre.Content = ConvertMarker(theBoard.Grid[2, 1]);
        }

        private void btn_bottomright_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(2, 2);
            btn_bottomright.Content = ConvertMarker(theBoard.Grid[2, 2]);
        }
    }
}
