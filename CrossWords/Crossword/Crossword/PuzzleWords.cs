using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows;

namespace Crossword
{
    public enum Direction
    {
        across,
        down,
    }

    public class PuzzleWord
    {       
        public String Word { get; private set; }
        public int Length { get; private set; }
        
        public int ClueNumber { get; private set; }
        public String Clue { get; private set; }

        public Direction WordDirection { get; private set; }
        public int StartColumn { get; private set; }
        public int StartRow { get; private set; }


        public PuzzleWord(string word, int cluenumber, string clue, string direction, int startC, int startR)
        {
            Word = word;
            Length = word.Length;

            ClueNumber = cluenumber;
            Clue = clue;            
            
            WordDirection = (Direction)Enum.Parse(typeof(Direction), direction.ToLower());
            StartColumn = startC;
            StartRow = startR;
        }

        public IEnumerable<char> GetLetters()
        {
            foreach (char item in Word)
            {
                yield return item;
            }
        }
    }

    public class PuzzleLetter : TextBox
    {
        public char ExpectedLetter { get; private set; }

        public PuzzleLetter(char expectedLetter)
        {
            ExpectedLetter = expectedLetter;
            this.MaxLength = 1;
            this.Text = "";
            this.FontSize = 24;
            this.HorizontalContentAlignment = HorizontalAlignment.Center;
            this.VerticalContentAlignment = VerticalAlignment.Center;
            this.CharacterCasing = CharacterCasing.Upper;
            this.Background = new SolidColorBrush(Colors.White);
            this.Foreground = new SolidColorBrush(Colors.Black);
        }

        public Boolean CheckLetter()
        {
            return ExpectedLetter == this.Text.Cast<char>().FirstOrDefault();
        }
    }
}
