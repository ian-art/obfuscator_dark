import re
import random
import base64
import sys

class BatchObfuscator:
    def __init__(self):
        self.var_map = {}
        self.var_counter = 0
        
    def generate_var_name(self):
        """Generate random variable names"""
        chars = 'abcdefghijklmnopqrstuvwxyz'
        length = random.randint(8, 15)
        return ''.join(random.choice(chars) for _ in range(length))
    
    def obfuscate_strings(self, code):
        """Obfuscate string literals using environment variables"""
        pattern = r'"([^"]+)"'
        
        def replace_string(match):
            original = match.group(1)
            if len(original) < 3:  # Don't obfuscate very short strings
                return match.group(0)
            
            var_name = self.generate_var_name()
            encoded = base64.b64encode(original.encode()).decode()
            
            # Store for later declaration
            self.var_map[var_name] = encoded
            return f'"%{var_name}%"'
        
        return re.sub(pattern, replace_string, code)
    
    def add_junk_code(self, lines):
        """Insert junk operations that don't affect execution"""
        junk_ops = [
            '@set {0}={1}',
            '@if %random% gtr 50000 (set {0}={1})',
            '@rem {0}',
        ]
        
        result = []
        for line in lines:
            result.append(line)
            if random.random() < 0.3:  # 30% chance to add junk
                junk = random.choice(junk_ops).format(
                    self.generate_var_name(),
                    random.randint(1, 9999)
                )
                result.append(junk)
        
        return result
    
    def obfuscate_commands(self, code):
        """Obfuscate common batch commands"""
        # Add random case mixing
        commands = ['echo', 'set', 'if', 'goto', 'call', 'for', 'rem']
        
        for cmd in commands:
            pattern = r'\b' + cmd + r'\b'
            # Randomly change case
            replacement = ''.join(
                c.upper() if random.random() > 0.5 else c.lower() 
                for c in cmd
            )
            code = re.sub(pattern, replacement, code, flags=re.IGNORECASE)
        
        return code
    
    def add_variable_indirection(self, code):
        """Add extra variable indirection"""
        lines = code.split('\n')
        result = []
        
        for line in lines:
            # Look for simple set commands
            match = re.match(r'@?set\s+(\w+)=(.+)', line, re.IGNORECASE)
            if match and random.random() < 0.4:
                var_name = match.group(1)
                value = match.group(2)
                temp_var = self.generate_var_name()
                
                result.append(f'@set {temp_var}={value}')
                result.append(f'@set {var_name}=%{temp_var}%')
            else:
                result.append(line)
        
        return '\n'.join(result)
    
    def obfuscate(self, batch_code):
        """Main obfuscation method"""
        print("[*] Starting obfuscation...")
        
        # Step 1: Obfuscate strings
        print("[*] Obfuscating strings...")
        code = self.obfuscate_strings(batch_code)
        
        # Step 2: Obfuscate command names
        print("[*] Obfuscating commands...")
        code = self.obfuscate_commands(code)
        
        # Step 3: Add variable indirection
        print("[*] Adding variable indirection...")
        code = self.add_variable_indirection(code)
        
        # Step 4: Add junk code
        print("[*] Inserting junk code...")
        lines = code.split('\n')
        lines = self.add_junk_code(lines)
        
        # Step 5: Build final output with variable declarations
        output = ['@echo off', '']
        
        # Add string variable declarations with decoding
        if self.var_map:
            output.append(':: Variable declarations')
            for var_name, encoded in self.var_map.items():
                # Create a simple decoder inline
                output.append(f'@set {var_name}={encoded}')
                # Note: Full base64 decode would require certutil or PowerShell
                # For demo, we'll use the encoded value directly
        
        output.append('')
        output.append(':: Main code')
        output.extend(lines)
        
        print("[+] Obfuscation complete!")
        return '\n'.join(output)


def main():
    print("=" * 60)
    print("Advanced Batch File Obfuscator")
    print("=" * 60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python obfuscator.py <input_file.bat> [output_file.bat]")
        print("\nExample:")
        print("  python obfuscator.py script.bat obfuscated.bat")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'obfuscated_' + input_file
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_code = f.read()
        
        print(f"[*] Reading input file: {input_file}")
        print(f"[*] Original size: {len(original_code)} bytes\n")
        
        obfuscator = BatchObfuscator()
        obfuscated_code = obfuscator.obfuscate(original_code)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)
        
        print(f"\n[*] Obfuscated size: {len(obfuscated_code)} bytes")
        print(f"[+] Output saved to: {output_file}")
        print("\n" + "=" * 60)
        print("Done!")
        
    except FileNotFoundError:
        print(f"[!] Error: File '{input_file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()