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

        private Grid CreateGrid(int ColumnCount, int RowCount, int Size)
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
            return CrossWordGrid;
        }

        private void mnuLoad_Click(object sender, RoutedEventArgs e)
        {
            var grid = CreateGrid(10, 10, 50);
            spMainPage.Children.Add(grid);

            //Read words from a file
            List<PuzzleWord> theList = new List<PuzzleWord>();
            theList.Add(new PuzzleWord("CAT", 1, "blabla", Direction.across.ToString(), 0, 2));

            //foreach word in puzzle
            foreach (PuzzleWord word in theList)
            {
                int startCol = word.StartColumn;
                int startRow = word.StartRow;

                //determine the direction
                int directionCol = Direction.across == word.WordDirection ? 1 : 0;
                int directionRow = Direction.down == word.WordDirection ? 1 : 0;

                //foreach character in the word
                foreach (char letter in word.GetLetters())
                {
                    TextBox box = new TextBox()
                    {
                        Text = "",
                        FontSize = 24,
                        HorizontalContentAlignment = HorizontalAlignment.Center,
                        VerticalContentAlignment = VerticalAlignment.Center,
                        CharacterCasing = CharacterCasing.Upper,
                        Background = new SolidColorBrush(Colors.White),
                        Foreground = new SolidColorBrush(Colors.Black),
                    };

                    //determine the starting position
                    Grid.SetColumn(box, startCol);
                    Grid.SetRow(box, startRow);

                    //move in the direction
                    startCol += directionCol;
                    startRow += directionRow;

                    grid.Children.Add(box);
                }

                //Add the clue to a list to display
            }

            //Create textbox if it doesn't already exist
            //Check expected letter if the textbox does exist
        }
    }
}
