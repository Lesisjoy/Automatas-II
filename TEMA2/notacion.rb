def PDP(dato)
    if dato == "+" || dato == "-"
        return 1
    elsif dato == "*" || dato == "/"
        return 2
    elsif dato == "^"
        return 3
    else
        return 0
    end
end

def solucion(expresion, pilaSalida)
    pila = []
    expresion.each_char do |c|
        if c.match?(/\w/) # Si es un número
            pilaSalida.push(c)
        elsif c == "+" || c == "-" || c == "*" || c == "/" || c == "^" || c == "("
            while !pila.empty? && PDP(pila.last) >= PDP(c) && pila.last != "("
                pilaSalida.push(pila.pop())
            end
            pila.push(c)
        elsif c == ")"
            while !pila.empty? && pila.last != "("
                pilaSalida.push(pila.pop())
            end
            pila.pop() if !pila.empty? && pila.last == "("
        end
    end
    while !pila.empty?
        pilaSalida.push(pila.pop())
    end
end

def evaluar(pila)
    pilaFinal = []
    pila.each do |c|
        if c == "+"
            num2 = pilaFinal.pop()
            num1 = pilaFinal.pop()
            pilaFinal.push(num1.to_f + num2.to_f)
        elsif c == "-"
            num2 = pilaFinal.pop()
            num1 = pilaFinal.pop()
            pilaFinal.push(num1.to_f - num2.to_f)
        elsif c == "*"
            num2 = pilaFinal.pop()
            num1 = pilaFinal.pop()
            pilaFinal.push(num1.to_f * num2.to_f)
        elsif c == "/"
            num2 = pilaFinal.pop()
            num1 = pilaFinal.pop()
            pilaFinal.push(num1.to_f / num2.to_f)
        elsif c == "^"
            num2 = pilaFinal.pop()
            num1 = pilaFinal.pop()
            pilaFinal.push(num1.to_f ** num2.to_f)
        else
            pilaFinal.push(c.to_f)
        end
    end
    puts "\nResultado:"
    puts pilaFinal[0]
end

pilaSalida = []
puts "Ingresa la expresion"
expresion = gets.chomp
puts "Expresion en posfijo:"
solucion(expresion, pilaSalida)
print pilaSalida
evaluar(pilaSalida)