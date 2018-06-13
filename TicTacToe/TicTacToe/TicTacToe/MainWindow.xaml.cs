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
    #region The converter for the buttons control
    public class MyConvertor : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            //How to convert string to int?
            string temp = value.ToString();

            Image theImage = new Image()
            {
                HorizontalAlignment = System.Windows.HorizontalAlignment.Center,
                VerticalAlignment = System.Windows.VerticalAlignment.Center,
                Source = new BitmapImage(new Uri("pack://application:,,,/Pictures/" + temp + ".png")),
            };
            return theImage;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
    #endregion

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        //Global Variables
        public Board theBoard;


        public double AdjustPosition(double buttonWidth, double topCorner, double coordinate)
        {
            var buttonWidthMultiplier = (buttonWidth / 2) * (2 * coordinate + 1);
            //The spacing between the blocks is 32 = btn_topleft.Width / 3
            var spacingWidthMultiplier = (buttonWidth / 3) * coordinate;

            return topCorner + buttonWidthMultiplier + spacingWidthMultiplier;
        }

        public void TriggerWin(Line theLine)
        {
            var top = btn_topleft.TranslatePoint(new Point(0, 0), this);
            var firstPoint = theLine.PointsList[0];
            var lastPoint = theLine.PointsList[theLine.PointsList.Count - 1];

            var drawingLine = new System.Windows.Shapes.Line()
            {
                HorizontalAlignment = HorizontalAlignment.Left,
                VerticalAlignment = VerticalAlignment.Center,
                StrokeThickness = 15,
                Stroke = Brushes.Green,
                X1 = AdjustPosition(btn_topleft.Width, top.X, firstPoint.Y),
                Y1 = AdjustPosition(btn_topleft.Height, top.Y, firstPoint.X),
                X2 = AdjustPosition(btn_topleft.Width, top.X, lastPoint.Y),
                Y2 = AdjustPosition(btn_topleft.Height, top.Y, lastPoint.X)
            };

            thegrid.Children.Add(drawingLine);

            lbl_message.Content = "WINNER";
            lbl_message.FontSize = 48;

            sp_BoardGrid.IsEnabled = false;
        }

        public void TriggerDraw(Line theLine)
        {
            lbl_message.Content = "Draw";
            lbl_message.FontSize = 48;

            sp_BoardGrid.IsEnabled = false;
        }

        public void TriggerRefresh(Line theLine)
        {
            lbl_message.Content = "";
            lbl_message.FontSize = 1;
            thegrid.Children.Clear();
            sp_BoardGrid.IsEnabled = true;
        }

        public void WinningState()
        {
            theBoard.PlaceMarker(2, 0); // X
            theBoard.PlaceMarker(1, 1); // O
            theBoard.PlaceMarker(1, 0); // X
            theBoard.PlaceMarker(0, 1); // O
            theBoard.PlaceMarker(2, 1); // X
            theBoard.PlaceMarker(0, 2); // O
        }

        public MainWindow()
        {
            InitializeComponent();

            theBoard = new Board(TriggerWin, TriggerDraw, TriggerRefresh);
            Main.DataContext = theBoard.theGrid;

            //WinningState();
        }

        #region Top row
        private void btn_topleft_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(0, 0);
        }

        private void btn_topcentre_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(0, 1);
        }

        private void btn_topright_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(0, 2);
        }
        #endregion

        #region Middle row
        private void btn_left_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(1, 0);
        }

        private void btn_centre_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(1, 1);
        }

        private void btn_right_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(1, 2);
        }
        #endregion

        #region Last row
        private void btn_bottomleft_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(2, 0);
        }

        private void btn_bottomcentre_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(2, 1);
        }

        private void btn_bottomright_Click(object sender, RoutedEventArgs e)
        {
            theBoard.PlaceMarker(2, 2);
        }
        #endregion

        private void Window_KeyDown(object sender, KeyEventArgs e)
        {
            switch (e.Key)
            {
                case Key.Clear:
                    theBoard.RefreshBoard();
                    break;
                case Key.F5:
                    theBoard.RefreshBoard();
                    break;
                default:
                    break;
            }
        }
    }
}
