using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TicTacToe
{
    public class Board
    {
        private char[,] _grid = new char[3, 3];
        private char _marker = 'X';

        public char[,] Grid => _grid;

        public Board()
        {
            for (int i = 0; i < 3; i++)
            {
                for (int k = 0; k < 3; k++)
                {
                    _grid[i, k] = 'B';
                }
            }
        }

        public void PlaceMarker(int x, int y)
        {
            if (((x < 3) || (y < 3)) && _grid[x,y] == 'B')
            {
                _grid[x, y] = _marker;
                _marker = (_marker == 'X') ? 'O' : 'X';

                //Check if that was a winning move
                //If it is trigger the win drawing event
            }

            //We don't want this to trigger an error cause the user might have just clicked here.
        }
    }
}
