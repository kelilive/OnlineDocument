# C / C++ Language Standards Timeline

| C | Year | C++ | Year |
|---|---|---|---|
| C89 / C90 | 1990 | C++98 | 1998 |
| C95 | 1995 | - | - |
| C99 | 1999 | C++03 | 2003 |
| C11 | 2011 | C++11 | 2011 |
| - | - | C++14 | 2014 |
| C17 | 2018 | C++17 | 2017 |
| - | - | C++20 | 2020 |
| C23 | 2024 | C++23 | 2024 |

---

## C89 / C90 (1990)

```c
/* block comments only */
int add(x, y)     /* old-style (K&R) function declaration */
int x, y;
{
    int result;
    result = x + y;
    return result;
}
```

Key additions: `volatile`, `enum`, `signed`, `void`, locales, `const` (from C++), function prototypes (from C++).

## C95 (1995)

```c
#include <wchar.h>
#include <wctype.h>

// digraphs: <% {  %> }  <: [  :> ]  %: #  %:%: ##

int main(void) {
    wchar_t wc = L'A';
    wchar_t ws[] = L"hello";

    wprintf(L"%ls\n", ws);

    if (iswupper(wc)) {
        wprintf(L"uppercase\n");
    }

    return 0;
}
```

Key additions: wide and multibyte character support (`<wchar.h>`, `<wctype.h>`), digraphs, `<iso646.h>`.

## C99 (1999)

```c
// single-line comments added

#include <stdbool.h>
#include <stdint.h>
#include <inttypes.h>

int add(int x, int y) {
    // declare anywhere, not just at block start
    for (int i = 0; i < 10; i++) {
        bool flag = true;        // _Bool via stdbool.h
        long long big = 1LL;     // long long

        printf("%d\n", i);
    }

    // designated initializers
    struct Point { int x; int y; };
    struct Point p = { .x = 10, .y = 20 };

    // compound literals
    func((int[]){ 1, 2, 3 });

    // restrict pointer
    // variable-length arrays (VLA)
    // flexible array members
    // variadic macros
    // inline functions
    // hexadecimal floating-point (%a)

    return x + y;
}
```

Key additions: `bool`, `long long`, `stdint.h`, `inttypes.h`, `restrict`, compound literals, VLA, flexible array members, designated initializers, variadic macros, `//` comments, `inline`, mix declarations and code, `snprintf`, `_Exit`, complex numbers.

## C11 (2011)

```c
#include <stdalign.h>
#include <stdatomic.h>
#include <stdnoreturn.h>
#include <threads.h>

// _Generic type-selection
#define type_name(x) _Generic((x), int: "int", double: "double", default: "other")

static_assert(sizeof(int) == 4, "int must be 4 bytes");
alignas(16) int aligned_array[4];
noreturn void fail(void) { while (1); }

// anonymous structs and unions
union {
    int i;
    float f;
};

// atomics
atomic_int counter = 0;

// threads
thrd_t thread_id;
int result;
```

Key additions: thread-aware memory model, `_Atomic`, `<threads.h>`, `_Generic`, `alignas`/`alignof`, `_Noreturn`, `static_assert`, anonymous structs/unions, `char16_t`/`char32_t`, `quick_exit`, bounds-checking interfaces.

## C17 (2018)

```c
// bug-fix release -- no new language features
// same as C11, only 54 defect fixes
// gets() finally removed
// __STDC_VERSION__ = 201710L
```

## C23 (2024)

```c
// bool, true, false are now keywords (no stdbool.h needed)
bool finished = false;

// nullptr keyword replaces NULL
int* ptr = nullptr;

// constexpr for compile-time constants
constexpr int size = 100;

// attributes (like C++ [[attr]])
[[deprecated("use new_func instead")]]
void old_func(void);

// static_assert with no message string required
static_assert(sizeof(int) == 4);

// improved enums with underlying type
enum Color : unsigned char { RED, GREEN, BLUE };

// preprocessor additions
// #elifdef / #elifndef
// #warning
// #embed (binary resource inclusion)
// __has_include, __has_c_attribute

// no K&R function declarations
// no implicit int
```

---

## C++98 (1998)

```cpp
#include <iostream>
#include <vector>
#include <string>

int main() {
    // classes, inheritance, virtual functions
    // templates
    // std::vector, std::string
    // exceptions: try / catch
    // namespace

    std::vector<int> v;
    v.push_back(42);

    std::string s = "hello";
    std::cout << s << std::endl;

    try {
        throw std::runtime_error("error");
    } catch (std::exception& e) {
        std::cerr << e.what() << std::endl;
    }

    return 0;
}
```

Key additions: RTTI (`dynamic_cast`, `typeid`), `bool`, `mutable`, covariant return types, STL (containers, algorithms, iterators, function objects), `string`, `iostream`, `auto_ptr`.

## C++03 (2003)

```cpp
// bug-fix release -- no new language features
// same as C++98
// value-initialization clarified (T() for POD)
// 92 core + 125 library defect fixes
```

## C++11 (2011)

```cpp
#include <iostream>
#include <vector>

int main() {
    // auto type deduction
    auto x = 42;

    // range-based for
    std::vector<int> v = {1, 2, 3};
    for (auto& elem : v) {
        elem *= 2;
    }

    // lambda
    auto add = [](int a, int b) -> int { return a + b; };

    // nullptr
    int* p = nullptr;

    // move semantics (std::move, &&)
    // smart pointers (std::unique_ptr, std::shared_ptr)
    // variadic templates
    // static_assert, override, final
    // enum class
    // constexpr, decltype

    return 0;
}
```

Key additions: `auto`, lambdas, move semantics, `nullptr`, `constexpr`, `decltype`, range-for, variadic templates, `std::unique_ptr`/`shared_ptr`, `enum class`, `override`/`final`, `unordered_map`/`set`, `<random>`, `<regex>`, `std::thread`.

## C++14 (2014)

```cpp
// generic lambdas
auto add = [](auto a, auto b) { return a + b; };

// auto return type deduction
auto func(void) { return 42; }

// std::make_unique
auto p = std::make_unique<int>(5);

// variable templates
template<typename T>
constexpr T pi = T(3.14159);

// digit separators
int million = 1'000'000;

// binary literals
int bits = 0b1010;
```

## C++17 (2017)

```cpp
#include <iostream>
#include <string>
#include <optional>
#include <string_view>

int main() {
    // structured bindings
    auto [a, b] = std::make_pair(1, "hello");

    // if constexpr
    if constexpr (sizeof(int) == 4) {
        std::cout << "32-bit int" << std::endl;
    }

    // std::optional, std::variant, std::any
    std::optional<std::string> maybe = "hello";
    std::string_view sv = "hello world";

    // fold expressions
    template<typename... Args>
    auto sum(Args... args) { return (... + args); }

    // nested namespaces: namespace A::B::C { }
    // filesystem library
    // parallel algorithms

    return 0;
}
```

Key additions: structured bindings, `if constexpr`, `std::optional`/`variant`/`any`, `string_view`, fold expressions, filesystem, parallel algorithms.

## C++20 (2020)

```cpp
#include <iostream>
#include <vector>
#include <ranges>
#include <concepts>

// concepts
template<typename T>
concept Addable = requires(T a, T b) { a + b; };

template<Addable T>
T add(T a, T b) { return a + b; }

int main() {
    // ranges library
    auto r = std::views::iota(1, 10)
           | std::views::filter([](int n) { return n % 2 == 0; });

    // coroutines (co_await, co_yield, co_return)
    // modules (import / export)
    // std::span
    // consteval, constinit
    // spaceship operator <=>
    // designated initializers (from C)

    // import std;  // modules (future)

    return 0;
}
```

Key additions: concepts, coroutines, ranges, modules, `std::span`, `consteval`/`constinit`, spaceship `<=>`, `std::format`.

## C++23 (2024)

```cpp
#include <print>
#include <expected>
#include <mdspan>

int main() {
    // std::print / std::println
    std::println("Hello {}!", "world");

    // std::expected
    std::expected<int, std::string> result = 42;

    // std::mdspan (multi-dimensional array view)
    // deducing this
    // if/while with consteval
    // multiline string literals
    // stacktrace library

    return 0;
}
```

Key additions: `std::print`/`println`, `std::expected`, `std::mdspan`, deducing this, `std::stacktrace`, `import std;`.

---

## Key Milestones

| Year | Language | Significance |
|---|---|---|
| 1990 | C89 / C90 | First ANSI/ISO C standard |
| 1995 | C95 | Wide chars, digraphs, internationalization |
| 1998 | C++98 | First ISO C++ standard |
| 1999 | **C99** | Modernized C: `//`, `for (int i)`, `long long`, designated init |
| 2003 | C++03 | Bugfix: value initialization, defect fixes |
| 2011 | **C++11** | Modernized C++: auto, lambdas, move, smart pointers |
| 2011 | C11 | `_Generic`, atomics, threads, static_assert |
| 2014 | C++14 | Generic lambdas, auto return, make_unique |
| 2017 | C++17 | Structured bindings, if constexpr, filesystem |
| 2018 | C17 | Bugfix only (54 defects) |
| 2020 | C++20 | Concepts, coroutines, ranges, modules |
| 2024 | C23 | `nullptr`, `bool` keyword, `constexpr`, attributes |
| 2024 | C++23 | `std::print`, `std::expected`, `mdspan`, deducing this |
