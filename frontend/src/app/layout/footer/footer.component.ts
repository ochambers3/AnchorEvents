import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [MatButtonModule, MatIconModule],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css'
})
export class FooterComponent {
  doSomething = (): void => {
    console.log('clicked');
  }

  openGithub = (): void => {
    window.open('https://github.com/ochambers3', '_blank');
  }

  openLinkedIn = (): void => {
    window.open('https://www.linkedin.com/in/owen-chambers33/', '_blank');
  }
}
