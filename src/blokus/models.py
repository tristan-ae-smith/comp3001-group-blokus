from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator, RegexValidator
from django.db import models
from datetime import datetime


class Game(models.Model):
	start_time = models.DateTimeField(default=datetime.now())
	game_type = models.IntegerField()
	player_turn = models.PositiveIntegerField(validators=[MaxValueValidator(3)], default=0)

	#def place_piece(self, piece):	#Places a piece and returns TRUE if the placement is valued, otherwise returns FALSE.

	def _validate_placement(self, piece):	#Returns TRUE if the placement is valid, FALSE otherwise.
		return (
			self._not_obstructed(piece) and
			self._adjacent_to_same_colour(piece)
		)

	def _not_obstructed(self, piece):	#Skeletal function
		return true

	def _adjacent_to_same_colour(self, piece):	#Skeletal function
		return true

class PieceMaster(models.Model):
	piece_data = models.CharField(max_length=12)	#Repretented by 'T', 'F' and ','; 'T' represents a block, 'F' represents no block, ',' represents newline.

	def get_bitmap(self):
		tup = []
		for row in self.piece_data.split(','):
			rowlist = []
			for letter in row:
				if letter == 'T':
					rowlist.append(True)
				elif letter == 'F':
					rowlist.append(False)
			tup.append(tuple(rowlist))
		return tuple(tup)

class UserProfile(models.Model):
	name = models.CharField(max_length=30)

	wins = models.IntegerField()
	losses = models.IntegerField()

	#def __init__(self, name, password):
	#Currently accepts 'master' with any username so functions can be worked on before authentication is implemented.

_colour_regex = r"^(red|yellow|green|blue)$"

class Player(models.Model):
	game = models.ForeignKey(Game)
	colour = models.CharField(max_length=6, validators=[RegexValidator(regex=_colour_regex)])
	user = models.ForeignKey(UserProfile)

class Piece(models.Model):
	master = models.ForeignKey(PieceMaster)
	player = models.ForeignKey(Player)

	x = models.PositiveIntegerField(validators=[MaxValueValidator(20)],null=True, default=0)
	y = models.PositiveIntegerField(validators=[MaxValueValidator(20)],null=True, default=0)

	rotation = models.PositiveIntegerField(validators=[MaxValueValidator(3)], default=0)
	flip = models.BooleanField(default=False) #Represents a TRANSPOSITION; flipped pieces are flipped along the axis runing from top left to bottom right.

	def get_bitmap(self):	#Returns the bitmap of the master piece which has been appropriately flipped and rotated.
		bitmap = self.master.get_bitmap()	#Need to implement rotation and transposition.
		return bitmap

	def flip(self, horizontal):	#Flips the piece horizontally; horizontal is a bool where T flips horizontally and F flips vertically.
		self.flip = not self.flip
		self.rotation = self.rotate(horizontal)

	def rotate(self, clockwise):	#Rotates the piece clockwise; 'clockwise' is a bool; T for clockwise rotation, F for anticlockwise.
		if (clockwise):
			self.rotation = (self.rotation + 1) % 4
		else:
			self.rotation = (self.rotation - 1) % 4

def _transpose_bitmap(bitmap):
	transposed_bitmap = []

	for row in range(0, len(bitmap)):
		transposed_row = []
		for col in range(0, len(bitmap[0])):
			transposed_row.append(bitmap[col][row])
		transposed_bitmap.append(tuple(transposed_row))

	return transposed_bitmap

def _rotate_bitmap(bitmap, times):
	rotated_bitmap = bitmap
	for time in range(times):
		for row in range(len(rotated_bitmap)):
			rotated_row = []
			for col in range(len(rotated_bitmap[0])):
				rotated_row.append(
					bitmap
						[(row + len(rotated_bitmap[0])) % len(rotated_bitmap)]
						[(col + len(rotated_bitmap)) % len(rotated_bitmap[0])]
					)
			rotated_bitmap.append(tuple(rotated_row))
	return rotated_bitmap
