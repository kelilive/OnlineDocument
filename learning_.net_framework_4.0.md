# Learning .NET Framework 4.0!

Understanding [.NET](https://learn.microsoft.com/en-us/dotnet/api/?view=netframework-4.8.1) namespaces is essential, as they effectively assist us in intuitively comprehending the structure of the .NET framework.

# `MsCorlib.dll` Namespaces

* [Microsoft.Win32](#!)⭐
  * [Microsoft.Win32.SafeHandles](#!)
* [System](#!)⭐
  * [System.Collections](#!)⭐
    * [System.Collections.Concurrent](#!)
    * [System.Collections.Generic](#!)⭐
      * [`class Comparer<T>`](#!)
      * [`class Dictionary<TKey,TValue>`](#!)
      * [`class EqualityComparer<T>`](#!)
      * [`interface ICollection<T>`](#!)
      * [`interface IComparer<in T>`](#!)
      * [`interface IDictionary<TKey,TValue>`](#!)
      * [`interface IEnumerable<out T>`](#!)
      * [`interface IEnumerator<out T>`](#!)
      * [`interface IEqualityComparer<in T>`](#!)
      * [`interface IList<T>`](#!)
      * [`interface IReadOnlyCollection<out T>`](#!)
      * [`interface IReadOnlyDictionary<TKey,TValue>`](#!)
      * [`interface IReadOnlyList<out T>`](#!)
      * [`class KeyNotFoundException`](#!)
      * [`struct KeyValuePair<TKey,TValue>`](#!)
      * [`class List<T>`](#!)
    * [System.Collections.ObjectModel](#!)⭐
      * [`class Collection<T>`](#!)
      * [`class KeyedCollection<TKey,TItem>`](#!)
      * [`class ReadOnlyCollection<T>`](#!)
      * [`class ReadOnlyDictionary<TKey,TValue>`](#!)
  * [System.Configuration.Assemblies](#!)
  * [System.Deployment.Internal](#!)
  * [System.Diagnostics](#!)
    * [System.Diagnostics.CodeAnalysis](#!)
    * [System.Diagnostics.Contracts](#!)
      * [System.Diagnostics.Contracts.Internal](#!)
    * [System.Diagnostics.SymbolStore](#!)
    * [System.Diagnostics.Tracing](#!)
  * [System.Globalization](#!)⭐
  * [System.IO](#!)⭐
    * [System.IO.IsolatedStorage](#!)
  * [System.Reflection](#!)⭐
    * [System.Reflection.Emit](#!)
  * [System.Resources](#!)
  * [System.Runtime](#!)
    * [System.Runtime.CompilerServices](#!)
    * [System.Runtime.ConstrainedExecution](#!)
    * [System.Runtime.DesignerServices](#!)
    * [System.Runtime.ExceptionServices](#!)
    * [System.Runtime.Hosting](#!)
    * [System.Runtime.InteropServices](#!)
      * [System.Runtime.InteropServices.ComTypes](#!)
      * [System.Runtime.InteropServices.Expando](#!)
      * [System.Runtime.InteropServices.WindowsRuntime](#!)
    * [System.Runtime.Remoting](#!)
      * [System.Runtime.Remoting.Activation](#!)
      * [System.Runtime.Remoting.Channels](#!)
      * [System.Runtime.Remoting.Contexts](#!)
      * [System.Runtime.Remoting.Lifetime](#!)
      * [System.Runtime.Remoting.Messaging](#!)
      * [System.Runtime.Remoting.Metadata](#!)
        * [System.Runtime.Remoting.Metadata.W3cXsd2001](#!)
      * [System.Runtime.Remoting.Proxies](#!)
      * [System.Runtime.Remoting.Services](#!)
    * [System.Runtime.Serialization](#!)
      * [System.Runtime.Serialization.Formatters](#!)
        * [System.Runtime.Serialization.Formatters.Binary](#!)
    * [System.Runtime.Versioning](#!)
  * [System.Security](#!)
    * [System.Security.AccessControl](#!)
    * [System.Security.Claims](#!)
    * [System.Security.Cryptography](#!)
      * [System.Security.Cryptography.X509Certificates](#!)
    * [System.Security.Permissions](#!)
    * [System.Security.Policy](#!)
    * [System.Security.Principal](#!)
  * [System.Text](#!)⭐
  * [System.Threading](#!)⭐
    * [System.Threading.Tasks](#!)

# `System.dll` Namespaces

* [Microsoft.CSharp](#!)
* [Microsoft.VisualBasic](#!)
* [Microsoft.Win32](#!)
  * [Microsoft.Win32.SafeHandles](#!)
* [System](#!)
  * [System.CodeDom](#!)
    * [System.CodeDom.Compiler](#!)
  * [System.Collections.Concurrent](#!)
  * [System.Collections.Generic](#!)⭐
    * [`interface ISet<T>`](#!)
    * [`class LinkedList<T>`](#!)
    * [`class LinkedListNode<T>`](#!)
    * [`class Queue<T>`](#!)
    * [`class SortedDictionary<TKey,TValue>`](#!)
    * [`class SortedSet<T>`](#!)
    * [`class Stack<T>`](#!)
  * [System.Collections.ObjectModel](#!)⭐
    * [class ObservableCollection<T>](#!)
    * [class ReadOnlyObservableCollection<T>](#!)
  * [System.Collections.Specialized](#!)
  * [System.ComponentModel](#!)
    * [System.ComponentModel.Design](#!)
      * [System.ComponentModel.Design.Serialization](#!)
  * [System.Configuration](#!)⭐
  * [System.Diagnostics](#!)
    * [System.Diagnostics.CodeAnalysis](#!)
  * [System.IO](#!)⭐
    * [System.IO.Compression](#!)⭐
    * [System.IO.Ports](#!)⭐
  * [System.Media](#!)
  * [System.Net](#!)⭐
    * [System.Net.Cache](#!)⭐
    * [System.Net.Configuration](#!)⭐
    * [System.Net.Mail](#!)⭐
    * [System.Net.Mime](#!)⭐
    * [System.Net.NetworkInformation](#!)⭐
    * [System.Net.Security](#!)⭐
    * [System.Net.Sockets](#!)⭐
    * [System.Net.WebSockets](#!)⭐
  * [System.Reflection](#!)
  * [System.Runtime.InteropServices](#!)
    * [System.Runtime.InteropServices.ComTypes](#!)
  * [System.Runtime.Versioning](#!)
  * [System.Security](#!)
    * [System.Security.AccessControl](#!)
    * [System.Security.Authentication](#!)
      * [System.Security.Authentication.ExtendedProtection](#!)
        * [System.Security.Authentication.ExtendedProtection.Configuration](#!)
    * [System.Security.Claims](#!)
    * [System.Security.Cryptography](#!)
      * [System.Security.Cryptography.X509Certificates](#!)
    * [System.Security.Permissions](#!)
  * [System.Text.RegularExpressions](#!)⭐
  * [System.Threading](#!)
  * [System.Timers](#!)⭐
  * [System.Web](#!)
  * [System.Windows.Input](#!)
  * [System.Windows.Markup](#!)

# `System.Core.dll` Namespaces

* [Microsoft.Win32.SafeHandles](#!)
* [System](#!)
  * [System.Collections.Generic](#!)⭐
    * [class HashSet<T>](#!)
  * [System.Diagnostics](#!)
    * [System.Diagnostics.Eventing](#!)
      * [System.Diagnostics.Eventing.Reader](#!)
    * [System.Diagnostics.PerformanceData](#!)
  * [System.Dynamic](#!)⭐
  * [System.IO](#!)
    * [System.IO.MemoryMappedFiles](#!)
    * [System.IO.Pipes](#!)⭐
  * [System.Linq](#!)⭐
    * [System.Linq.Expressions](#!)⭐
  * [System.Management.Instrumentation](#!)
  * [System.Runtime.CompilerServices](#!)
  * [System.Runtime.InteropServices](#!)
  * [System.Security](#!)
    * [System.Security.Cryptography](#!)
      * [System.Security.Cryptography.X509Certificates](#!)
  * [System.Threading](#!)
    * [System.Threading.Tasks](#!)