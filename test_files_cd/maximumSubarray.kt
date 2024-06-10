package aula01

//porque não se muda após construção.
data class Triple(val left: Int, val sum: Double, val right: Int)


/**
 * This solution is quadratic.
 * @param array The changes of prices in consecutive days
 * @param left The first day to consider
 * @param right The last day to consider
 * @return An object which describes what is the subarray (array,l,r) where the sum is maximum within the subarray (array,left,right)
 */
//TPC aula prática
fun maximumSubArrayQuadratic(array: DoubleArray, left: Int, right: Int): Triple {
    var l = left
    var r = left - 1
    var bestSum = 0.0
    var actualSum: Double
    for (i in left..right) {
        actualSum = 0.0
        for (j in i..right) {
            actualSum += array[j]
            if (bestSum < actualSum) { //it case of more than one solution, it keeps the first one.
                bestSum = actualSum
                r = j
                l = i
            }
        }
    }
    return Triple(l, bestSum, r)
}

/**
 * This solution is linear (N).
 * Kadane Algorithm
 * @param array The changes of prices in consecutive days
 * @param left The first day to consider
 * @param right The last day to consider
 * @return An object which describes what is the subarray (array,l,r) where the sum is maximum within the subarray (array,left,right)
 */
fun maximumSubArrayLinear(array: DoubleArray, left: Int, right: Int): Triple {
    var bestLeft = left
    var actualLeft = left
    var bestRight = left - 1
    var bestSum = 0.0
    var actualSum = 0.0
    for (i in left..right) {
        actualSum += array[i]
        if (actualSum > bestSum) {
            bestSum = actualSum
            bestLeft = actualLeft
            bestRight = i
        } else {
            if (actualSum < 0) {
                actualLeft = i + 1
                actualSum = 0.0
            }
        }
    }
    return Triple(bestLeft, bestSum, bestRight)
}
