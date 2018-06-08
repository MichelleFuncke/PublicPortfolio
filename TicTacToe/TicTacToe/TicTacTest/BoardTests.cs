using NUnit.Framework;
using System;
using TicTacToe;

namespace TicTacTest
{
    [TestFixture]
    public class BoardTests
    {
        ///MethodName_StateUnderTest_ExpectedBehavior
        ///https://dzone.com/articles/7-popular-unit-test-naming

        [TestCase(0, 0)]
        [TestCase(0, 1)]
        [TestCase(2, 1)]
        public void PlaceMarker_BoardAfterConstructor_MarkerAtXY(int x, int y)
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
