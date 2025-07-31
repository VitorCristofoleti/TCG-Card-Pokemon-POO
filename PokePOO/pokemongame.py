from pokemon import Pokemon, pokemons
from time import sleep
import random
import os
import platform
import copy
from colorama import init
from termcolor import colored


# Função para limpar a tela dependendo do sistema operacional
def limpar_tela():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

class Selecao:
    def mostrar_todos(self):
        print("\n📜 Lista de todos os Pokémons disponíveis:\n")
        for i, p in enumerate(pokemons):
            print(colored(f"{i+1}.", "cyan"), colored(p.nome, "yellow", attrs=['bold']))
            print(p.ascii_art)
            sleep(1)

    def selecionarpokemons(self):
        # Sorteia 6 pokémons aleatórios
        deck_completo = [copy.deepcopy(p) for p in random.sample(pokemons, 6)]
        print("\n🧩 Seus 6 Pokémons sorteados:")
        for i, p in enumerate(deck_completo):
            print(f"{colored(f'{i+1}.', 'yellow', attrs=['bold'])} {colored(p.nome, 'cyan', attrs=['bold'])}")
            print(p.ascii_art)
            sleep(1)

        # Jogador escolhe 3 pokémons para o deck final
        print("\n🎯 Escolha 3 Pokémons (pelo número) para batalhar:")
        escolha = []
        while len(escolha) < 3:
            try:
                num = int(input(f"Escolha {len(escolha)+1}: "))
                if 1 <= num <= 6 and num-1 not in escolha:
                    escolha.append(num-1)
                else:
                    print(colored("❌ Escolha inválida ou repetida.", "black","on_red",attrs=['bold']))
            except ValueError:
                print(colored("❌ Digite um número válido.","black","on_red",attrs=['bold']))
        deck_escolhido = [deck_completo[i] for i in escolha]
        print("\n✅ Seu deck final:")
        for p in deck_escolhido:
            print(colored(f"- {p.nome}", "cyan", attrs=['bold']))
            print(p.ascii_art)
        return deck_escolhido

class PvP:
    def __init__(self, deck1, deck2):
        self.rodada = 0
        self.deck1 = deck1
        self.deck2 = deck2
        self.historico = []

    def mostrar_deck(self, deck, jogador):
        if jogador == 1:
            cor_jogador = 'blue'
        elif jogador == 2:
            cor_jogador = 'red'
        else:
            cor_jogador = 'white' #isso aqui n vai acontecer mas só pra completar o if

        print(f"\n🔹 {colored(f'Pokémons do Jogador {jogador}', cor_jogador, attrs=['bold'])}:")

        for i, p in enumerate(deck):
            barra = colored(f"█" * (p.vida // 10), "green", attrs=['bold']) + \
                    colored("-", 'red',attrs=['bold']) * (10 - p.vida // 10)
            
            print(f"{colored(i+1,'cyan',attrs=['bold'])}. {colored(p.nome, 'yellow', attrs=['bold'])} "
                  f"{colored('Vida:', 'green', attrs=['bold'])} "
                  f"{colored(p.vida, 'white', 'on_green', attrs=['bold'])} "
                  f"[{barra}], {colored('ATK', 'red', attrs=['bold'])}: {colored(p.attack, 'white', 'on_red', attrs=['bold'])}, "
                  f"{colored('DEF', 'cyan', attrs=['bold'])}: {colored(p.def_, 'cyan', 'on_blue', attrs=['bold'])})")
            
    def escolher_pokemon(self, deck, jogador):
        vivos = [p for p in deck if p.vida > 0]
        tentativas = 3
        while tentativas > 0:
            self.mostrar_deck(vivos, jogador)
            try:
                escolha = int(input(f"🎯 Jogador {jogador}, escolha um Pokémon: ")) - 1
                if 0 <= escolha < len(vivos):
                    return vivos[escolha]
                else:
                    print(colored("❌ Escolha inválida.", "black", "on_red", attrs=['bold']))
            except ValueError:
                print(colored("❌ Digite um número.", "black", "on_red", attrs=['bold']))
            tentativas -= 1
        print(colored("⚠️ Escolha automática feita.", 'yellow', attrs=['bold']))
        return vivos[0]

    def realizar_ataque(self, atacante, defensor):
        if atacante in self.deck1:
            cor_atacante = 'blue'
            cor_defensor = 'red'
        else:
            cor_atacante = 'red'
            cor_defensor = 'blue'
        dano = max(atacante.attack - defensor.def_, 0) + 10
        defensor.vida = max(defensor.vida - dano, 0)
        self.historico.append(
            f"{colored(atacante.nome, cor_atacante, attrs=['bold'])} atacou {colored(defensor.nome, cor_defensor, attrs=['bold'])} causando {colored(str(dano), 'white', 'on_red', attrs=['bold'])} de dano.")
        print(f"⚔️ {colored(atacante.nome, cor_atacante, attrs=['bold'])} atacou {colored(defensor.nome, cor_defensor, attrs=['bold'])} causando {colored(dano, 'white','on_red', attrs=['bold'])} de dano!")
        if defensor.vida == 0:
            print(colored(f"💀 {defensor.nome} desmaiou!", 'grey', attrs=['bold']))
            self.historico.append(colored(f"💀 {defensor.nome} desmaiou!",'grey', attrs=['bold']))

    def executar_rodada(self, p1, p2):
        self.rodada += 1
        self.historico.append(colored(f"\n===🎯 Rodada {self.rodada}===",'yellow',attrs=['bold']))
    
        print(f"\n🆚 {colored(p1.nome, 'yellow', attrs=['bold'])} {colored('Jogador 1', 'blue', attrs=['bold'])} vs {colored(p2.nome, 'yellow', attrs=['bold'])} {colored('Jogador 2', 'red', attrs=['bold'])}")

        if random.choice([True, False]):
            print(f"🎲 {colored('Jogador 1', 'blue', attrs=['bold'])} começa a rodada!")
            self.realizar_ataque(p1, p2)
            if p2.vida > 0:
                self.realizar_ataque(p2, p1)
        else:
            print(f"🎲 {colored('Jogador 2', 'red', attrs=['bold'])} começa a rodada!")
            self.realizar_ataque(p2, p1)
            if p1.vida > 0:
                self.realizar_ataque(p1, p2)




    def exibir_resultado(self):
        print(colored("\n🏁 Fim da batalha!\n",'cyan',attrs=['bold']))
        for evento in self.historico:
            print(evento)

        vivos1 = sum(1 for p in self.deck1 if p.vida > 0)
        vivos2 = sum(1 for p in self.deck2 if p.vida > 0)

        if vivos1 > vivos2:
            print(f"🏆 {colored('Jogador 1', 'blue', attrs=['bold'])} venceu!")
        elif vivos2 > vivos1:
            print(f"🏆 {colored('Jogador 2', 'red', attrs=['bold'])} venceu!")
        else:
            print(colored("🤝 Empate!",'yellow',attrs=['bold']))



    def batalhar(self):
        print("\n⚔️ Iniciando a batalha!")
        while any(p.vida > 0 for p in self.deck1) and any(p.vida > 0 for p in self.deck2):
            print(colored("\n========== NOVA RODADA ==========",'yellow',attrs=['bold']))
            p1 = self.escolher_pokemon(self.deck1, 1)
            p2 = self.escolher_pokemon(self.deck2, 2)
            self.executar_rodada(p1, p2)
        self.exibir_resultado()

# Executando o jogo
if __name__ == "__main__":
    selecao = Selecao()
    while True:
        print(colored("\n=== MENU PRINCIPAL ===",'cyan',attrs=['bold']))
        print(colored("1. Mostrar todos os Pokémons","yellow", attrs=['bold']))
        print(colored("2. Iniciar Batalha", "blue",attrs=['bold']))
        print(colored("3. Sair","red",attrs=['bold']))
        opcao = input("Escolha: ")

        if opcao == "1":
            selecao.mostrar_todos()
        elif opcao == "2":
            print(f"\n🎮 {colored('Jogador 1','blue',attrs=['bold'])}, sua vez:")
            deck1 = selecao.selecionarpokemons()
            input(f"\n🔁 Passe para o {colored('Jogador 2', 'red',attrs=['bold'])} e pressione {colored('ENTER','yellow','on_black')} para limpar a tela...")
            limpar_tela()  # Limpa a tela após a escolha do Jogador 1
            print(f"\n🎮 {colored('Jogador 2','red',attrs=['bold'])}, sua vez:")
            deck2 = selecao.selecionarpokemons()
            input(f"\n🔁 Passe para o {colored('Jogador 1','blue',attrs=['bold'])} e pressione {colored('ENTER','yellow','on_black')} para limpar a tela...")
            limpar_tela()  # Limpa a tela após a escolha do Jogador 2
            iniciar = input(f"\n🚀 Iniciar batalha agora? ({colored('s', 'green')}/{colored('n','red')}): ").strip().lower()
            if iniciar == "s":
                PvP(deck1, deck2).batalhar()
            elif iniciar == 'n':
                print("🔙 Voltando ao menu.")
            else:
                print(colored("Selecione apenas uma das opções acima.", 'yellow',attrs=['bold']))
        elif opcao == "3":
            print("👋 Até a próxima!")
            break
        else:
            print(colored("❌ Opção inválida.", "on_red"))
