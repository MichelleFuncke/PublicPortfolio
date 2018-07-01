using Crossword.PopupWindows;
using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
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
using System.Xml.Serialization;

namespace Crossword
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        CrossWord Puzzle;

        public MainWindow()
        {
            InitializeComponent();
        }

        #region Ready puzzles
        private void Puzzle1()
        {
            Puzzle = new CrossWord(18, 9, 50);

            //across
            Puzzle.Add(new PuzzleWord("MOTORWORKS", 1, "Get a $13.95 oil charge", Direction.across.ToString(), 8, 2));
            Puzzle.Add(new PuzzleWord("CULVERS", 3, "Remodeling to serve you better", Direction.across.ToString(), 0, 6));
            Puzzle.Add(new PuzzleWord("HEWITT", 4, "Jackson ____. Pay $50 less this year", Direction.across.ToString(), 12, 6));
            Puzzle.Add(new PuzzleWord("VINNYSPIZZA", 5, "Home of the 24\" hurricane pizza", Direction.across.ToString(), 4, 8));
            Puzzle.Add(new PuzzleWord("CARPETLANDUSA", 2, "With your tax refund get carpet", Direction.across.ToString(), 0, 4));

            //down
            Puzzle.Add(new PuzzleWord("GIORDANOS", 2, "\"Love Takes Many Forms\"", Direction.down.ToString(), 9, 0));
            Puzzle.Add(new PuzzleWord("ROSS", 3, "Hanser ___. A leader in eye care", Direction.down.ToString(), 11, 1));
            Puzzle.Add(new PuzzleWord("MIKIMOTO", 4, "Japanese steakhouse in Dekalls featuring hibachi dinners", Direction.down.ToString(), 16, 0));
            Puzzle.Add(new PuzzleWord("BELLAS", 1, "Featuring a \"Fairy Dust Fun Station\"", Direction.down.ToString(), 6, 1));
        }

        private void Puzzle2()
        {
            Puzzle = new CrossWord(18, 13, 50);

            //across
            Puzzle.Add(new PuzzleWord("ULLRICH", 1, "__ Law, Estate Planning, Wills, Trusts, Elder law", Direction.across.ToString(), 10, 2));
            Puzzle.Add(new PuzzleWord("DENTAL", 3, "__ Fields. Family & Cosmetic Dentistry", Direction.across.ToString(), 12, 4));
            Puzzle.Add(new PuzzleWord("GARLISCH", 4, "__ Automotive Services, Inc, $13.50 oil change", Direction.across.ToString(), 3, 5));
            Puzzle.Add(new PuzzleWord("FUNME", 2, "Excursions and Entertainment", Direction.across.ToString(), 1, 3));
            Puzzle.Add(new PuzzleWord("MEDITERRANEO", 5, "Middle Eastern Sunday Buffet $11.95", Direction.across.ToString(), 3, 8));
            Puzzle.Add(new PuzzleWord("KISHHEALTHSYSTEM", 6, "Now part of Northwestern Medicine", Direction.across.ToString(), 0, 10));
            Puzzle.Add(new PuzzleWord("RUBYSASIAN", 7, "__ __ Market & Other Importal Goods", Direction.across.ToString(), 8, 12));

            //down
            Puzzle.Add(new PuzzleWord("JAMRAH", 2, "Chicken Shawarma Meal Deal, $7.99", Direction.down.ToString(), 4, 1));
            Puzzle.Add(new PuzzleWord("LOSSCENTER", 3, "Sycamore Integrated Weight __ __.", Direction.down.ToString(), 8, 3));
            Puzzle.Add(new PuzzleWord("MULCHWORKS", 4, "Where hundreds receive great service every year", Direction.down.ToString(), 10, 1));
            Puzzle.Add(new PuzzleWord("HARVEST", 5, "__ Bible Chapel. Good Friday 7pm", Direction.down.ToString(), 13, 0));
            Puzzle.Add(new PuzzleWord("LEHAN", 6, "We're more than medicine", Direction.down.ToString(), 17, 4));
            Puzzle.Add(new PuzzleWord("QUALITY", 1, "__ Mattress Warehouse. Get a free queen", Direction.down.ToString(), 1, 6));
        }
        #endregion

        #region Create puzzle
        private void mnuCreate_Click(object sender, RoutedEventArgs e)
        {
            tabWindow.SelectedItem = tbiCreatePuzzle;

            if (Puzzle != null)
            {
                //Can't just remove Puzzle.TheGrid because it might be a new instance

                //Find the location of the button just before the grid
                var buttonIndex = spMakePuzzle.Children.IndexOf(btnDrawGrid);
                //Remove everything after this button
                spMakePuzzle.Children.RemoveRange(buttonIndex + 1, 4);
            }

            Puzzle = new CrossWord(10, 10, 40, true);
            spMakePuzzle.Children.Add(Puzzle.TheGrid);
            udColumn.Value = Puzzle.Columns;
            udRow.Value = Puzzle.Rows;

            lbClues.ItemsSource = Puzzle.Words;
        }

        private void btnResize_Click(object sender, RoutedEventArgs e)
        {
            var col = (int)udColumn.Value;
            var row = (int)udRow.Value;

            spMakePuzzle.Children.Remove(Puzzle.TheGrid);

            Puzzle.ResizeGrid(col, row, 40, true);

            spMakePuzzle.Children.Add(Puzzle.TheGrid);
        }

        private void btnADD_Click(object sender, RoutedEventArgs e)
        {
            var Pop = new AddWindow((int)udColumn.Value, (int)udRow.Value);
            if ((bool)Pop.ShowDialog())
            {
                //Add the word to the list of words to draw
                Puzzle.Add(Pop.Word);   
            } 
        }

        private void btnEDIT_Click(object sender, RoutedEventArgs e)
        {
            //Edit an existing clue
            var word = lbClues.SelectedItem as PuzzleWord;
            var Pop = new EditWindow(word, (int)udColumn.Value, (int)udRow.Value);
            if ((bool)Pop.ShowDialog())
            {
                word.Populate(Pop.Word);
            }
        }

        private void btnREMOVE_Click(object sender, RoutedEventArgs e)
        {
            //Remove from the list
            Puzzle.Remove(lbClues.SelectedItem as PuzzleWord);
        }

        private void btnDrawGrid_Click(object sender, RoutedEventArgs e)
        {
            //Empty the grid
            Puzzle.ClearGrid();

            Puzzle.DrawPuzzle();

            if (Puzzle.InvalidWords.Count() > 0)
            {
                MessageBox.Show("Some words weren't drawn because they were invalid");
            } 
        }
        #endregion

        #region Solve Puzzle
        private void mnuLoad_Click(object sender, RoutedEventArgs e)
        {
            tabWindow.SelectedItem = tbiSolvePuzzle;

            if (Puzzle != null)
            {
                //Can't just remove Puzzle.TheGrid because it might be a new instance

                //Find the location of the button just before the grid
                var cluesIndex = spMain.Children.IndexOf(lbClues2);
                //Remove everything after this button
                spMain.Children.RemoveRange(cluesIndex + 1, 4);
                lbClues2.ItemsSource = null;
            }

            OpenFileDialog openFile = new OpenFileDialog();
            openFile.Title = "Open CrossWord";
            openFile.Filter = "eXtensible Markup Language file|*.xml";

            if ((bool)openFile.ShowDialog())
            {
                var file = new FileInfo(openFile.FileName);
                Puzzle = new CrossWord(file, 50);
                Puzzle.Sort();

                spMain.Children.Add(Puzzle.TheGrid);

                Puzzle.DrawPuzzle();

                if (Puzzle.InvalidWords.Count() > 0)
                {
                    MessageBox.Show("Some words weren't drawn because they were invalid");
                }

                lbClues2.ItemsSource = Puzzle.Words;
            } 
        }

        private void btnReset_Click(object sender, RoutedEventArgs e)
        {
            if (Puzzle == null)
            {
                return;
            }

            foreach (PuzzleLetter item in Puzzle.TheGrid.Children)
            {
                item.Text = "";
            }

            Puzzle.TheGrid.Background = new SolidColorBrush(Colors.Black);
        }

        private void btnCheck_Click(object sender, RoutedEventArgs e)
        {
            if (Puzzle == null)
            {
                return;
            }

            var solved = true;
            foreach (PuzzleLetter item in Puzzle.TheGrid.Children)
            {
                solved = item.CheckLetter() && solved;
            }

            if (!solved)
            {
                Puzzle.TheGrid.Background = new SolidColorBrush(Colors.Red);
            }
        }
        #endregion

        private void mnuSave_Click(object sender, RoutedEventArgs e)
        {
            if (Puzzle == null)
            {
                return;
            }

            SaveFileDialog saveFile = new SaveFileDialog();
            saveFile.Title = "Save CrossWord";
            saveFile.Filter = "eXtensible Markup Language file|*.xml";

            if ((bool)saveFile.ShowDialog())
            {
                var file = new FileInfo(saveFile.FileName);
                Puzzle.Save(file);
            }  
        }
    }
}
