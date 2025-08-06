import { Component } from '@angular/core';
import { SearchCriteriaService, PopupService } from '../../../housing.service';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-events',
  standalone: true,
  imports: [MatIconModule, MatChipsModule, MatInputModule, MatFormFieldModule, MatButtonModule, FormsModule],
  templateUrl: './events.component.html',
  // styleUrl: './events.component.css'
  styleUrl: '../pop-up.css'
})
export class EventsComponent {
  // If all event types are false, then they are all true. Else it is all true events.
  artists: string[] = [];
  artist: string = '';
  music: boolean = false;
  sports: boolean = false;

  constructor(private searchCriteria: SearchCriteriaService, private popupService: PopupService) {
    const existing = this.searchCriteria.getCriteria();
  }

  saveMusic() {
    this.music = !this.music;
  }

  addArtist() {
    if (this.artist.trim() && !this.artists.includes(this.artist.trim())) {
      this.artists.push(this.artist.trim());
      this.artist = '';
    }
  }

  removeArtist(c: string) {
    this.artists = this.artists.filter(x => x !== c);
  }

  saveArtist() {
    this.sports = !this.music;
  }

  saveChoice() {
    this.searchCriteria.setEvents(this.artists);
    this.popupService.closePopup();
    console.log('Artists saved:', this.artists);
  }
}
