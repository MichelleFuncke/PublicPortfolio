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

        [TestCase(1, 0)]
        [TestCase(0, 1)]
        [TestCase(2, 1)]
        public void PlaceMarker_BoardAfterTwoValidMarkers_MarkerAtXY(int x, int y)
        {
            //Arrange
            var actual = new Board();
            actual.PlaceMarker(0, 0);
            actual.PlaceMarker(2, 0);

            //Act
            actual.PlaceMarker(x, y);

            //Assert
            Assert.AreEqual('X', actual.Grid[x, y]);
        }

        [TestCase(1, 0, true)]
        [TestCase(0, 0, false)]
        [TestCase(2, 0, false)]
        [TestCase(5, 0, false)]
        [TestCase(2, 6, false)]
        public void IsFreeSpace_BoardAfterTwoValidMarkers_Boolean(int x, int y, bool expected)
        {
            //Arrange
            var actual = new Board();
            actual.PlaceMarker(0, 0);
            actual.PlaceMarker(2, 0);

            //Act\Assert
            Assert.AreEqual(expected, actual.IsFreeSpace(x, y));
        }
    }
}
