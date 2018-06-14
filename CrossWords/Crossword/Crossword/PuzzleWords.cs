using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

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
            startC = StartColumn;
            startR = StartRow;
        }

        public IEnumerable<char> GetLetters()
        {
            foreach (char item in Word)
            {
                yield return item;
            }
        }
    }

    public class PuzzleLetter
    {
        public char ExpectedLetter { get; private set; }
        public char Letter { get; set; }

        public PuzzleLetter(char expected)
        {
            ExpectedLetter = expected;
        }

        public Boolean CheckLetter()
        {
            return ExpectedLetter == Letter;
        }
    }
}
