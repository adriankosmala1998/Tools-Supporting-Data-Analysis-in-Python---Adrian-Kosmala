import argparse

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-i","--input", help="File with text to be repeated, default: input.txt", default = 'input.txt')
parser.add_argument("-n","--num", help="Number of repetitions of text, need to be positive integer, default: 1", default = 1, type=int)
parser.add_argument("-o","--output", help="Output file with repeated text, default: output.txt", default = 'output.txt')

args = parser.parse_args()

def multiply_string(input_file, repeat_number, output_file):
   with open(input_file, 'r') as r_f, open(output_file, 'w') as w_f:
      input_text = r_f.read()
      output_text = ""
      for i in range(repeat_number):
         output_text = output_text + input_text

      w_f.write(output_text)


   print('INPUT TEXT:')
   print(input_text)
   print("NUMBER OF REPETITIONS:")
   print(repeat_number)
   print('OUTPUT TEXT:')
   print(output_text)

multiply_string(args.input, args.num, args.output)
