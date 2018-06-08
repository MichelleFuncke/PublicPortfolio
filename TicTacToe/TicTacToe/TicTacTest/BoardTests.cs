using NUnit.Framework;
using System;
using TicTacToe;

namespace TicTacTest
{
    [TestFixture]
    public class BoardTests
    {
        [TestCase(0,0)]
        public void EmptyBoard_noError(int x, int y)
        {
            //Arrange
            var actual = new Board();

            //Act
            actual.PlaceMarker(x, y);

            //Assert
            Assert.AreEqual('X', actual.Grid[x,y]);
        }
    }
}
