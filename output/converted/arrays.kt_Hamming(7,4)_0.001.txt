package parte1

fun squaresSorted(v: IntArray): IntArray {
    // if (v.isEmpty()) return null
    if (v.isEmpty()) return v
    val novo = IntArray(v.size)
    var v1: Int
    var v2: Int
    var i = 0
    var j = v.size - 1
    var z = j
    while (i <= j) {
        v1 = v[i] * v[i]
        v2 = v[j] * v[j]
        if (v1 >= v2) {
            novo[z--] = v1
            i++
        } else {
            novo[z--] = v2
            j--
        }
    }
    return novo
}

fun counter(array:IntArray, k:Int, lower:Int, upper:Int):Pair<Int,Int> {
    var currentSum:Int = 0;
    var first= 0;
    var second=0;
    if(k<=array.size && array.size!=0) {
        for( i in 0 until k-1) currentSum += array[i];
    for (i in k - 1 until array.size) {
        currentSum += array[i];
        if (currentSum < lower) {
            first+=1
        } else if (currentSum > upper) {
            second += 1;
        }
        currentSum -= array[i - k + 1];
    }
    }
    return Pair(first,second);
}
fun sumGivenN(n: Int): Int {
    if (n == 0) return 1
    var start = 1
    var end = 1
    var sum = 1
    var count = 0
    while (start <= n) {
        if (sum < n) {
            end += 1
            sum += end
        } else if (sum > n) {
            sum -= start
            start += 1
        } else if (sum == n) {
            for (i in start..end) {
                print(i)
            }
            count++
            println()
            sum -= start
            start += 1
        }
    }
    return count
}

fun myCompare(s1:String, s2:String):Int{
    var i = 0
    var j = s2.length - 1
    while (i <= j) {
        if (s1[i] != s2[j]) return s1[i] - s2[j]
        i++
        j--
    }
    return if (s1.length == s2.length) 0 else s1.length - s2.length
}


fun countInverses(v: Array<String>, l: Int, r: Int): Int {
    val naturalOrder =
        Comparator { s1: String, s2: String? -> s1.compareTo(s2!!) }
    quicksort(v, l, r, naturalOrder)
    var count = 0
    for (i in 0..r) {
        var x = i + 1
        var y = r
        while (x <= y) {
            val mid = (x + y) / 2
            val c = myCompare(v[mid], v[i])
            if (c == 0) {
                count++
                break
            } else if (c > 0) y = mid - 1 else x = mid + 1
        }
    }
    return count
}



private fun partition(a: IntArray, l: Int, r: Int): Int {
    val x = a[r]
    var i = l - 1
    for (j in l until r) {
        if (a[j] <= x) {
            i++
            exch(a, i, j)
        }
    }
    i++
    exch(a, r, i)
    return i
}

private fun exch(v: IntArray, l: Int, pivot: Int) {
    val aux = v[pivot]
    v[pivot] = v[l]
    v[l] = aux
}

private fun quicksort(a: Array<String>, l: Int, r: Int, cmp: Comparator<String>) {
    val partition: Int
    if (l < r) {
        partition = partition(a, l, r, cmp)
        quicksort(a, l, partition - 1, cmp)
        quicksort(a, partition + 1, r, cmp)
    }
}

private fun partition(a: Array<String>, l: Int, r: Int, cmp: Comparator<String>): Int {
    val x = a[r]
    var i = l - 1
    for (j in l until r) {
        if (cmp.compare(a[j], x) <= 0) {
            i++
            exchange(a, i, j)
        }
    }
    i++
    exchange(a, r, i)
    return i
}

fun exchange(v: Array<String>, i: Int, j: Int) {
    val tmp = v[i]
    v[i] = v[j]
    v[j] = tmp
}

fun countInRange(v1: IntArray, l: Int, r: Int, min: Int, max: Int): Int {
    val num = 0
    val mid = l + (r - l) / 2
    if (v1.size == 0) return num
    // if (l < 0 || r > v1.size - 1) throw UnsupportedOperationException()
    return if (v1[l] >= min && v1[r] <= max) r - l + 1 else
        leftBound(v1, l, min, max, mid) + rightBound(v1, r, max, min, mid + 1)
}

// devia ser logaritmico
fun rightBound(v1: IntArray, r: Int, max: Int, min: Int, mid: Int): Int {
    var mid = mid
    var count = 0
    while (mid <= r) {
        if (v1[mid] <= max && v1[mid] >= min) ++count
        ++mid
    }
    return count
}

// devia ser logaritmico
fun leftBound(v1: IntArray, l: Int, min: Int, max: Int, mid: Int): Int {
    var mid = mid
    var count = 0
    while (mid >= l) {
        if (v1[mid] >= min && v1[mid] <= max) ++count
        --mid
    }
    return count
}


// Auxiliary methods
//......