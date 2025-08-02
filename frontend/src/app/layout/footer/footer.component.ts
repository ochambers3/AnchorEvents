import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
// import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [MatButtonModule, MatIconModule],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css'
})
export class FooterComponent {
  // constructor(
  //   private matIconRegistry: MatIconRegistry,
  //   private domSanitizer: DomSanitizer
  // ) {
  //   this.matIconRegistry.addSvgIcon(
  //     'github',
  //     this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/github.svg')
  //   );
  // }

  doSomething = (): void => {
    console.log('clicked');
  }
}
