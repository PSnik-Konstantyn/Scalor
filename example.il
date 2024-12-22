// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly example
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module example.exe

// Definition of Program class.
.class private auto ansi beforefieldinit Program
  extends [mscorlib]System.Object
{
    .method private hidebysig static void Main(string[] args) cil managed
    {
    .locals (
       [0]  float32 n10     )
   .entrypoint
   //.maxstack  8
   ldloca    n10
   ldc.r4    1.0
   stind.r4
   ldloca    n10
   ldloc    n10
   ldc.i4    2
   conv.r4
   ldc.r4    2.1
   ldc.i4    2
   conv.r4
   conv.r8
   call   float64 [mscorlib]System.Math::Pow(float64, float64)
   call   float64 [mscorlib]System.Math::Pow(float64, float64)
   add
   stind.r4
   ldloc    n10
   call void [mscorlib]System.Console::WriteLine(float32)
   call    string [mscorlib]System.Console::ReadLine()
   call float32 [mscorlib]System.Single::Parse(string)
   stloc n10
   ldloc    n10
   call void [mscorlib]System.Console::WriteLine(float32)
   ldloc    n10
   ldc.i4    2
   conv.r4
   cgt
   brfalse    m1
   ldloc    n10
   call void [mscorlib]System.Console::WriteLine(float32)
   br    m2
m1:
   ldloca    n10
   ldloc    n10
   ldc.r4    10.0
   add
   stind.r4
   ldloc    n10
   call void [mscorlib]System.Console::WriteLine(float32)
m2:
m3:
   ldloc    n10
   ldc.i4    3
   conv.r4
   cgt
   brfalse    m4
   ldloc    n10
   call void [mscorlib]System.Console::WriteLine(float32)
   ldloca    n10
   ldloc    n10
   ldc.r4    1.0
   sub
   stind.r4
   br    m3
m4:
	ret    
}
}