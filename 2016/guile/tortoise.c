/* Simple backend for a Logo like tortoise drawer.  */

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <math.h>

static const int WIDTH = 10;
static const int HEIGHT = 10;

static FILE*
start_gnuplot ()
{
  FILE* output;
  int pipes[2];
  pid_t pid;

  pipe (pipes);
  pid = fork ();

  if (!pid)
    {
      dup2 (pipes[0], STDIN_FILENO);
      execlp ("gnuplot", NULL);
      return; /* Not reached.  */
    }

  output = fdopen (pipes[1], "w");

  fprintf (output, "set multiplot\n");
  fprintf (output, "set parametric\n");
  fprintf (output, "set xrange [-%d:%d]\n", WIDTH, WIDTH);
  fprintf (output, "set yrange [-%d:%d]\n", HEIGHT, HEIGHT);
  fprintf (output, "set size ratio -1\n");
  fprintf (output, "unset xtics\n");
  fprintf (output, "unset ytics\n");
  fflush (output);

  return output;
}

static FILE* global_output;

int
main (int argc, char* argv[])
{
  global_output = start_gnuplot ();
  tortoise_reset();

  {
      int i;
      tortoise_pendown (); /* This is unnecessary, but makes it clearer.  */
      for (i = 1; i <= 4; ++i)
          {
              tortoise_move (3.0);
              tortoise_turn (90.0);
          }
  }
  
  return EXIT_SUCCESS;
}

static void
draw_line (FILE* output, double x1, double y1, double x2, double y2)
{
  fprintf (output, "plot [0:1] %f + %f * t, %f + %f * t notitle\n",
           x1, x2 - x1, y1, y2 - y1);
  fflush (output);
}

static double x, y;
static double direction;
static int pendown;

static void
tortoise_reset ()
{
  x = y = 0.0;
  direction = 0.0;
  pendown = 1;

  fprintf (global_output, "clear\n");
  fflush (global_output);
}

static void
tortoise_pendown ()
{
  pendown = 1;
}

static void
tortoise_penup ()
{
  pendown = 0;
}

static void
tortoise_turn (double degrees)
{
  direction += M_PI / 180.0 * degrees;
}

static void
tortoise_move (double length)
{
  double newX, newY;

  newX = x + length * cos (direction);
  newY = y + length * sin (direction);

  if (pendown)
    draw_line (global_output, x, y, newX, newY);

  x = newX;
  y = newY;
}
