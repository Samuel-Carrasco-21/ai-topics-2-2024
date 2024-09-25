from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
import math

class RaceEnum(Enum):
  orc = "ORC"
  elf = "ELF"
  human = "HUMAN"
  globin = "GOBLIN"

class Guild(BaseModel):
  id:int | None = None
  name: str
  realm: str
  created: datetime
  used: bool

class Character(BaseModel):
  id:int | None = None
  name: str
  level: int
  race: RaceEnum
  hp: int
  damage: int
  guild_id: int

app = FastAPI(title="validation")

guilds = []
characters = []

@app.get("/guilds", status_code=200)
def get_guilds():
  return guilds

@app.get("/characters", status_code=200)
def get_characters():
  return characters

@app.post("/guilds", status_code=201)
def create_guild(guild: Guild):
  id = len(guilds) + 1
  guild.id = id
  guild.used = False
  guilds.append(guild)
  return guild

@app.post("/characters", status_code=201)
def create_character(character: Character):
  id = len(characters) + 1
  character.id = id
  guild_id = character.guild_id
  index, guild = next(((index, guild) for index, guild in enumerate(guilds) if guild.id == character.guild_id), (None, None))
  if not guild:
    raise HTTPException(status_code=404, detail=f"Guild with id {guild_id} not found")
  if guild.used:
    raise HTTPException(status_code=405, detail=f"Guild with id {guild_id} already in use")
  guild.used = True
  guild[index] = guild
  characters.append(character)
  return character

@app.patch("/characters", status_code=200)
def update_character(id_character: int, updated_character: Character, update_guild: Guild | None):
  character = next((char for char in characters if char.id == id_character), None)
  
  if not character:
    raise HTTPException(status_code=404, detail=f"Character with id {id_character} not found")
  
  character.name = updated_character.name or character.name
  character.level = updated_character.level or character.level
  character.race = updated_character.race or character.race
  character.hp = updated_character.hp or character.hp
  character.damage = updated_character.damage or character.damage

  if id_guild is not None and update_guild is not None:
    guild_gotten = next((guild for guild in guilds if guild.id_guild == id_guild), None)
    
    if not guild_gotten:
      raise HTTPException(status_code=404, detail=f"Guild with id {id_guild} not found")
    
    guild_gotten.name = update_guild.name or guild_gotten.name
    guild_gotten.realm = update_guild.realm or guild_gotten.realm
    guild_gotten.created = update_guild.created or guild_gotten.created
  
  return character

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("models_api:app", reload=True, port=8008)
