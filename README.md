# Instalación

Antes de ejecutar el main.py, es necesario tener las siguientes librerías:

customtkinter

tkcalendar

Se pueden instalar con:

```python
pip install customtkinter tkcalendar
```

# Código en GCL

## DataManager.py

Se transcribe los principales algoritmos al pseudocódigo GCL creado por Dijkstra.

### Función LoadData

fun loadData(file_path: string) ret data: map
  if ¬os.path.exists(file_path) →
    data := {"tasks": [], "events": [], "lessons": []}
  [] os.path.exists(file_path) →
    file, err := open(file_path, "r", "utf-8");
    if err ≠ nil →
      print("Error al cargar el archivo JSON...");
      data := {"tasks": [], "events": [], "lessons": []}
    [] err = nil →
      raw_data, json_err := json.load(file);
      if json_err ≠ nil →
        print("Error al decodificar el JSON...");
        data := {"tasks": [], "events": [], "lessons": []}
      [] json_err = nil →
        tasks_data := raw_data.get('tasks', []);
        events_data := raw_data.get('events', []);
        lessons_data := raw_data.get('lessons', []);

        tasks_list := [];
        for task_item in tasks_data →
          tasks_list.append(Task.from_dict(task_item))
        rof;

        events_list := [];
        for event_item in events_data →
          events_list.append(Event.from_dict(event_item))
        rof;

        lessons_list := [];
        for lesson_item in lessons_data →
          lessons_list.append(Lesson.from_dict(lesson_item))
        rof;

        data := {"tasks": tasks_list, "events": events_list, "lessons": lessons_list}
      fi
    fi
  fi

### Función saveData()

fun saveData(self: DataManager)
  serializable_data := {
    "tasks": [],
    "events": [],
    "lessons": []
  };

  for t in self.data["tasks"] →
    serializable_data["tasks"].append(t.to_dict())
  rof;
  for e in self.data["events"] →
    serializable_data["events"].append(e.to_dict())
  rof;
  for l in self.data["lessons"] →
    serializable_data["lessons"].append(l.to_dict())
  rof;

  file, err := open(self.file_path, "w", "utf-8");
  if err ≠ nil →
    print("Error al guardar los datos...")
  [] err = nil →
    json.dump(serializable_data, file, indent=4)
  fi

### review_lesson()

fun review_lesson(self: Lesson, score: int) ret result: map
  if score < 3 →
    self.repetitions := 0;
    self.interval := 1
  [] score ≥ 3 →
    if self.repetitions = 0 →
      self.interval := 1
    [] self.repetitions = 1 →
      self.interval := 6
    [] self.repetitions > 1 →
      self.interval := ceil(self.interval * self.efactor)
    fi;
    self.repetitions := self.repetitions + 1;

    self.efactor := self.efactor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02));
    if self.efactor < 1.3 →
      self.efactor := 1.3
    fi
  fi;

  if score ≤ 1.3 and self.efactor < 1.3 →
    self.efactor := 1.3
  fi;

  self.next_review_date := today() + timedelta(days=self.interval);

  result := {
    "efactor": self.efactor,
    "interval": self.interval,
    "repetitions": self.repetitions,
    "next_review_date": self.next_review_date
  }

### addTask()

fun addTask(self: DataManager, title: string, due_date: date)
  new_task := Task(title, due_date);
  self.data["tasks"].append(new_task);
  self.saveData()

### deleteTask() (y practicamente todos los delete)

fun deleteTask(self: DataManager, index: int) ret success: bool
  if 0 ≤ index and index < len(self.data['tasks']) →
    del self.data['tasks'][index];
    self.saveData();
    success := True
  [] ¬(0 ≤ index and index < len(self.data['tasks'])) →
    success := False
  fi

### get_all_tasks()

fun get_all_tasks(self: DataManager) ret tasks: list
  tasks := self.data['tasks']


### addEvent()


fun addEvent(self: DataManager, title: string, description: string, due_date: date, time: string)
  new_event := Event(title, description, due_date, time);
  self.data['events'].append(new_event);
  self.saveData()

### `addEvent`
Agrega un nuevo evento a la lista y guarda los datos.

fun addEvent(self: DataManager, title: string, description: string, due_date: date, time: string)
  new_event := Event(title, description, due_date, time);
  self.data['events'].append(new_event);
  self.saveData()

### `deleteEvent`
Elimina un evento por su índice y guarda los datos.

fun deleteEvent(self: DataManager, index: int) ret success: bool
  if 0 ≤ index and index < len(self.data['events']) →
    del self.data['events'][index];
    self.saveData();
    success := True
  [] ¬(0 ≤ index and index < len(self.data['events'])) →
    success := False
  fi

### `get_all_events`
Retorna la lista de todos los eventos.

fun get_all_events(self: DataManager) ret events: list
  events := self.data['events']

---

## 📌 Métodos para Lecciones

### `addLesson`
Agrega una nueva lección a la lista y guarda los datos.

fun addLesson(self: DataManager, title: string, notes: string, due_date: date, subject: string)
  new_lesson := Lesson(title, notes, due_date, subject);
  self.data['lessons'].append(new_lesson);
  self.saveData()

### `deleteLesson`
Elimina una lección por su índice y guarda los datos.

fun deleteLesson(self: DataManager, index: int) ret success: bool
  if 0 ≤ index and index < len(self.data['lessons']) →
    del self.data['lessons'][index];
    self.saveData();
    success := True
  [] ¬(0 ≤ index and index < len(self.data['lessons'])) →
    success := False
  fi

### `reviewLesson`
Actualiza una lección después de un repaso y guarda los datos.

fun reviewLesson(self: DataManager, score: int, index: int) ret success: bool
  if 0 ≤ index and index < len(self.data['lessons']) →
    self.data['lessons'][index].review_lesson(score);
    self.saveData();
    success := True
  [] ¬(0 ≤ index and index < len(self.data['lessons'])) →
    print("Hubo un error, no se pudo actualizar.");
    success := False
  fi

### `get_all_lessons`
Retorna la lista de todas las lecciones.

fun get_all_lessons(self: DataManager) ret lessons: list
  lessons := self.data['lessons']

## Clase de Lessons.py

class Lesson

  # 📌 Constructor
  fun __init__(self: Lesson, title: string, notes: string, due_date: date, subject: string, interval: int, repetitions: int, efactor: float, next_review_date: date)
    self.title := title;
    self.notes := notes;
    self.due_date := due_date;
    self.subject := subject;
    self.repetitions := int(repetitions);
    self.efactor := float(efactor);
    self.interval := int(interval);
    self.next_review_date := next_review_date;

    if next_review_date = nil →
      creation_date := date.fromisoformat(self.due_date);
      self.next_review_date := creation_date + timedelta(days=1)
    [] next_review_date ≠ nil →
      if isinstance(next_review_date, str) →
        self.next_review_date := date.fromisoformat(next_review_date)
      [] ¬isinstance(next_review_date, str) →
        self.next_review_date := next_review_date
      fi
    fi

  # 📌 Representación en string
  fun __str__(self: Lesson) ret s: string
    s := "Clase: " + self.title + " | Materia: " + self.subject + " | Fecha: " + self.due_date

  # 📌 Conversión a diccionario
  fun to_dict(self: Lesson) ret d: map
    d := {
      'title': self.title,
      'notes': self.notes,
      'due_date': str(self.due_date),
      'subject': self.subject,
      'efactor': self.efactor,
      'repetitions': self.repetitions,
      'next_review_date': str(self.next_review_date),
      'interval': self.interval
    }

  # 📌 Construcción desde diccionario
  fun from_dict(data: map) ret l: Lesson
    l := Lesson(
      data['title'],
      data['notes'],
      data['due_date'],
      data['subject'],
      interval:=data.get('interval', 0),
      repetitions:=data.get('repetitions', 0),
      efactor:=data.get('efactor', 2.5),
      next_review_date:=data.get('next_review_date')
    )

end

Prácticamente las otras dos clases, (Task y Events) no cambian en cuanto a la estructura de sus algoritmos, puesto que ellos no tienne una función como la de reviewLesson()

### función reviewLesson() (de Lesson.py)

fun review_lesson(self: Lesson, score: int) ret result: map
  if score < 3 →
    self.repetitions := 0;
    self.interval := 1
  [] score ≥ 3 →
    if self.repetitions = 0 →
      self.interval := 1
    [] self.repetitions = 1 →
      self.interval := 6
    [] self.repetitions > 1 →
      self.interval := ceil(self.interval * self.efactor)
    fi;
    self.repetitions := self.repetitions + 1;
    self.efactor := self.efactor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02));
    if self.efactor < 1.3 →
      self.efactor := 1.3
    fi
  fi;

  if score ≤ 1.3 and self.efactor < 1.3 →
    self.efactor := 1.3
  fi;

  self.next_review_date := today() + timedelta(days=self.interval);
  result := {
    "efactor": self.efactor,
    "interval": self.interval,
    "repetitions": self.repetitions,
    "next_review_date": self.next_review_date
  }